#!/usr/bin/env python3
"""Construit le site autonome de « Mon Coach Maison » (application installable) dans /tmp/claude-0/site."""
import os, re, shutil, json, hashlib, sys

SRC = '/home/claude/coach-maison.html'
OUT = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/site'
THREE = '/tmp/claude-0/t3d/package/build/three.min.js'

s = open(SRC, encoding='utf-8').read()

# 1. fichiers réellement utilisés
vids = sorted(set(re.findall(r'"(vx/[a-f0-9]+\.mp4)"', s)))
photo_ids = set(re.findall(r'"[^"]+": "([A-Za-z0-9_\-]+)"', s[s.index('const PHOTO='):s.index('\n', s.index('const PHOTO='))]))
for d in ('vx', 'ex', 'icons'):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
for v in vids:
    shutil.copy2(os.path.join('/home/claude', v), os.path.join(OUT, v))
nph = 0
for pid in photo_ids:
    for i in (0, 1):
        f = f'ex/{pid}-{i}.webp'
        if os.path.exists(os.path.join('/home/claude', f)):
            shutil.copy2(os.path.join('/home/claude', f), os.path.join(OUT, f)); nph += 1
shutil.copy2(THREE, os.path.join(OUT, 'three.min.js'))

# 2. page complète : en-tête (titre, polices, styles) puis le corps de l'appli
s = s.replace('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', 'three.min.js')
s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
cut = s.index('</style>') + len('</style>')
head, body = s[:cut], s[cut:]
ver = hashlib.sha1(s.encode()).hexdigest()[:10]
page = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="Sweat Home, ton coach sportif à la maison : programme selon ta forme, ton temps et ton matériel.">
<meta name="theme-color" content="#F6EFE4" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#17120F" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Sweat Home">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="icons/favicon-32.png">
<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
{head}
</head>
<body>
{body}
<script>
// application installable : fonctionne aussi hors connexion une fois ouverte
if('serviceWorker' in navigator)addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{{}}));
</script>
</body>
</html>
'''
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page)

# 3. manifeste
json.dump({
    "name": "Sweat Home", "short_name": "Sweat Home", "lang": "fr",
    "description": "Le sport à la maison : programme selon ta forme, ton temps et ton matériel.",
    "start_url": "./", "scope": "./", "display": "standalone", "orientation": "portrait",
    "background_color": "#F4EBDD", "theme_color": "#D4582A",
    "icons": [
        {"src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
    ]
}, open(os.path.join(OUT, 'manifest.webmanifest'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# 4. service worker : la page et le moteur 3D en cache, vidéos et photos mises en cache à la première lecture
open(os.path.join(OUT, 'sw.js'), 'w').write(f'''const V='cm-{ver}',SHELL=['./','index.html','three.min.js','manifest.webmanifest','icons/icon-192.png','icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V&&x!=='cm-media').map(x=>caches.delete(x)))).then(()=>self.clients.claim()))}});
self.addEventListener('fetch',e=>{{
  const u=new URL(e.request.url);if(e.request.method!=='GET')return;
  // page : réseau d'abord pour recevoir les mises à jour, cache si hors connexion
  if(e.request.mode==='navigate'){{e.respondWith(fetch(e.request).then(r=>{{const c=r.clone();caches.open(V).then(x=>x.put('index.html',c));return r}}).catch(()=>caches.match('index.html')));return}}
  if(u.origin!==location.origin)return;
  // vidéos : laissées au navigateur (lecture par morceaux)
  if(u.pathname.endsWith('.mp4'))return;
  if(/\\/ex\\//.test(u.pathname)){{e.respondWith(caches.open('cm-media').then(c=>c.match(e.request).then(h=>h||fetch(e.request).then(r=>{{if(r.ok)c.put(e.request,r.clone());return r}}))));return}}
  e.respondWith(caches.match(e.request).then(h=>h||fetch(e.request)));
}});
''')

# 5. réglages d'hébergement (Netlify) : bons types et cache des fichiers lourds
open(os.path.join(OUT, '_headers'), 'w').write('''/vx/*
  Cache-Control: public, max-age=31536000, immutable
/ex/*
  Cache-Control: public, max-age=31536000, immutable
/sw.js
  Cache-Control: no-cache
/index.html
  Cache-Control: no-cache
/manifest.webmanifest
  Content-Type: application/manifest+json
''')
tot = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fs in os.walk(OUT) for f in fs)
print(f'{len(vids)} vidéos, {nph} photos, version {ver}, total {tot/1e6:.1f} Mo')
