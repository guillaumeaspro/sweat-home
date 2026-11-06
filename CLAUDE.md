# Sweat Home

Appli web de sport à la maison (ex « Mon Coach Maison »). Elle génère une séance du jour selon la forme de l'utilisateur, son temps disponible et le matériel qu'il a chez lui.

## Public et usage
- D'abord pour moi, puis ouverte à des testeurs (amis, proches), qui doivent pouvoir l'utiliser sans compte Claude.
- Usage principal sur téléphone, juste avant ou pendant la séance.

## Stack
- Appli en une seule page HTML/CSS/JS, sans framework ; mannequin 3D avec three.js (`three.min.js`).
- Appli installable (PWA) : `manifest.webmanifest`, `sw.js` pour le hors-connexion.
- Médias : photos d'exercices dans `ex/`, vidéos de démonstration dans `vx/`.
- Pas de compte ni de serveur : les données restent dans le navigateur de chaque personne.
- Hébergement : GitHub Pages (dépôt guillaumeaspro/sweat-home).

## Mise à jour
- On modifie `source/sweat-home-source.html` (version de travail), jamais `index.html` à la main.
- `source/build_site.py` génère le site (page, manifeste, hors-connexion) à la racine. Ses chemins sont codés en dur : les adapter avant de le lancer.
- Puis publier sur `main` et `gh-pages`.

## Identité visuelle
- Nom : Sweat Home
- Logo : maison terracotta + haltère, sur fond crème
- Palette : terracotta, crème

## Règles
- Mobile first : tout doit être confortable sur un écran de téléphone, boutons larges, peu de texte.
- Interface 100 % en français, ton motivant et simple.
- Je ne suis pas développeur : explique les changements en langage clair, sans jargon.
- Tu t'occupes de la mise en ligne et des mises à jour (commit + push) : je ne veux rien avoir à faire à la main.
- Ne pas ajouter de dépendance ou de service payant sans me demander.
- Avant de modifier une fonctionnalité utilisée par les testeurs, vérifie que rien ne casse.

## Retours testeurs
Quand je remonte des retours, classe-les (bug / amélioration / idée), propose un ordre de priorité, puis corrige.
