# Source de l'appli

- `sweat-home-source.html` : la version de travail de l'appli (identique à la version publiée sur Claude).
- `build_site.py` : transforme ce fichier en site installable (page complète, manifeste, mode hors connexion) à la racine du dépôt.

Pour une mise à jour : modifier `sweat-home-source.html`, lancer `build_site.py`, puis publier sur `main` et `gh-pages`.
