# Historique des versions

## garmin-1.0.0 · 2026-11-15

Fork pour Garmin, en lecture seule.

- Données Garmin lues par Claude et écrites dans la base de l'artifact (`sync/latest`, `laps/<date>`) ; la page n'a plus aucun accès à la montre.
- Plus d'envoi du plan sur la montre : le plan vit dans le dashboard.
- Bilan de séance calculé à partir des tours écrits par Claude, ressenti d'après le RPE Garmin.
- Sécurité : échappement de tout texte affiché, injection du COACH sécurisée (`kit/inject-coach.py`), plus de coordonnées GPS des sorties (météo à la ville), plus de Google Fonts.
- Démo régénérée (`exemples/build-demo.py`).

## 1.0.0 · 2026-10-13

Première version publique.

- Plan sur mesure envoyé sur la montre COROS, avec zones à la FC au seuil et allures Daniels.
- Calendrier vertical : fiche de séance en modale, appui long pour déplacer ou échanger, conseils de cohérence.
- Forme du jour (feu vert, orange, rouge), alléger ou renforcer une séance, bilan prévu / réalisé.
- Progression aérobie à FC fixe, VFC, FC de repos, sommeil, charge.
- Facultatif : météo des sorties et du jour de course (Open-Meteo), renfo, fiche Jour J, frise de saison, bilan du dimanche.
- Démo autonome avec un athlète fictif (`exemples/demo.html`).
