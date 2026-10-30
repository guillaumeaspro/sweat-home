const V='cm-9cef6949c2',SHELL=['./','index.html','three.min.js','manifest.webmanifest','icons/icon-192.png','icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(SHELL)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V&&x!=='cm-media').map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);if(e.request.method!=='GET')return;
  // page : réseau d'abord pour recevoir les mises à jour, cache si hors connexion
  if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put('index.html',c));return r}).catch(()=>caches.match('index.html')));return}
  if(u.origin!==location.origin)return;
  // vidéos : laissées au navigateur (lecture par morceaux)
  if(u.pathname.endsWith('.mp4'))return;
  if(/\/ex\//.test(u.pathname)){e.respondWith(caches.open('cm-media').then(c=>c.match(e.request).then(h=>h||fetch(e.request).then(r=>{if(r.ok)c.put(e.request,r.clone());return r}))));return}
  e.respondWith(caches.match(e.request).then(h=>h||fetch(e.request)));
});
