# Kit coach course à pied avec Claude et Garmin

Ce kit te donne un coach : il analyse tes données Garmin, cale tes zones cardiaques, construit un plan pour ta course et te monte un dashboard. Tu peux y déplacer ou échanger une séance (appui long sur la tuile), l'alléger ou la renforcer. Il te dit si tu es en forme pour la séance du jour, compare le prévu et le réalisé après chaque séance et affiche la météo. En option : renfo, fiche Jour J, frise de saison, bilan du dimanche.

**Lecture seule** : rien n'est envoyé sur ta montre ni sur ton compte Garmin.

## Ce qu'il te faut

- Claude avec l'outil Artifact (Claude Code, ou Cowork sur claude.ai).
- Un connecteur Garmin (serveur MCP) qui lit Garmin Connect.
- Facultatif : le connecteur **Open-meteo** pour la météo.

## Installation (5 minutes)

1. Dans Claude, crée un projet, par exemple « Course à pied ».
2. Ajoute les trois fichiers du kit : `GUIDE-CLAUDE.md`, `coach-dashboard-template.html`, `inject-coach.py`.
3. Écris : **« Lance le kit coach course »**.
4. Réponds aux questions. Claude te présente tes zones, son diagnostic et le plan avant de publier le dashboard.

## Bon à savoir

- Les données se mettent à jour quand tu demandes à Claude « mets à jour mon coach » (ou chaque jour avec une tâche planifiée). La page elle-même ne se connecte pas à Garmin.
- Pour que le bilan de séance compare bien chaque étape, appuie sur « lap » à chaque changement d'étape, ou crée la séance dans Garmin Connect.
- Ouvre le dashboard depuis Claude (barre latérale ou galerie) : c'est là qu'il lit sa base.
- Ne partage pas le lien du dashboard : il contient ta FC, ta VFC, ton sommeil et tes notes.
