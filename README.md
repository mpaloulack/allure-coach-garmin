# allure-coach-garmin

*Coach de course à pied pour **Garmin**, dans Claude. Fork de [allure-coach](https://github.com/Sekiro-kost/allure-coach) (conçu pour COROS).*

Un coach qui lit tes données Garmin, cale tes zones cardiaques, construit un plan pour ta course et te monte un dashboard : plan, forme du jour, bilan de chaque séance, progression aérobie, météo, fiche Jour J.

**Différence avec l'original : tout est en lecture seule.** Rien n'est envoyé sur la montre ni sur ton compte Garmin. Le plan vit dans le dashboard ; si tu veux être guidé au poignet pour une séance, tu la crées toi-même dans Garmin Connect.

> **Projet indépendant.** Non affilié à Garmin, COROS ni Anthropic. Ce n'est **pas un avis médical** : les plans sont des propositions à adapter à ton ressenti. En cas de douleur, arrête et consulte un professionnel de santé.

## Essayer sans rien installer

Ouvre [`exemples/demo.html`](exemples/demo.html) dans ton navigateur (télécharge le fichier, puis double-clic). Athlète fictif, aucune donnée lue ni écrite, dates recalées sur la semaine en cours.

## Ce que ça fait

- **Plan sur mesure** : zones sur ta FC au seuil (Friel), allures Daniels, séances variées, polarisation 80/20, affûtage.
- **Calendrier** : touche une séance pour sa fiche, appui long pour la déplacer ou l'échanger, avec des conseils si l'enchaînement devient risqué.
- **Forme du jour** : feu vert, orange ou rouge d'après la VFC (avec ta plage normale Garmin), le sommeil, la charge, la disposition à l'entraînement (Training Readiness) et ton ressenti.
- **Bilan de séance** : prévu contre réalisé à partir des tours de ta montre, avec ta note et la douleur éventuelle.
- **Progression aérobie** : ton allure à FC fixe, avec l'effet de la chaleur.
- **Facultatif** : météo (Open-Meteo), renfo, fiche Jour J avec prévision du départ, frise de saison, bilan du dimanche.

## Ce qu'il te faut

- Claude avec l'outil Artifact et sa base de données (ArtifactData) : Claude Code, ou Cowork sur claude.ai.
- Un **connecteur Garmin** (serveur MCP) qui lit Garmin Connect. Les outils varient selon le connecteur : le guide dit à Claude quoi chercher, pas quels noms utiliser.
- Facultatif : le connecteur **Open-meteo**.

## Installation

1. Crée un projet dans Claude, par exemple « Course à pied ».
2. Ajoute les fichiers du dossier [`kit/`](kit) : `GUIDE-CLAUDE.md`, `coach-dashboard-template.html` et `inject-coach.py`.
3. Écris : **« Lance le kit coach course »**.
4. Réponds aux questions (course, date, objectif, jours disponibles, ville d'entraînement). Claude te présente tes zones, son diagnostic et le plan, puis publie le dashboard.
5. Pour actualiser les données : **« mets à jour mon coach »** (ou une tâche planifiée quotidienne).

## Comment ça marche

```
Connecteur Garmin ──(lecture)──> Claude ──(ArtifactData)──> base de l'artifact <──(lecture)── dashboard
                                                                                   Open-Meteo (météo, ville seulement)
```

La page n'a **aucun** accès à Garmin : c'est Claude qui lit Garmin et écrit les données (`sync/latest`, `laps/<date>`) dans la base de l'artifact. La page n'appelle que le connecteur Open-Meteo, avec la position de ta ville. Tout ce qui est propre à l'athlète vit dans l'objet `COACH`, injecté dans le modèle HTML par `inject-coach.py`. Schéma complet : [`kit/GUIDE-CLAUDE.md`](kit/GUIDE-CLAUDE.md), exemple : [`exemples/exemple-coach.json`](exemples/exemple-coach.json).

## Vie privée et sécurité

Voir [`SECURITY.md`](SECURITY.md). En bref :
- lecture seule sur Garmin, la page elle-même n'y a pas accès ;
- aucune coordonnée GPS des sorties stockée : la météo utilise la ville (arrondie à environ 10 km) ;
- tout texte venant des données est échappé avant affichage (un nom d'activité piégé ne peut pas exécuter de code) ;
- pas de police Google ni d'autre ressource externe au chargement ;
- le dashboard est privé : **ne partage pas son lien**, il contient tes données de santé.

## Différences avec allure-coach

| | allure-coach (COROS) | allure-coach-garmin |
|---|---|---|
| Envoi du plan sur la montre | oui | non (lecture seule) |
| Accès de la page à la montre | lecture + écriture COROS | aucun |
| Mise à jour des données | la page, à l'ouverture | Claude, sur demande ou planifiée |
| Position pour la météo | départ de chaque sortie (~1 km) | ville fixe (~10 km) |
| Échappement du texte affiché | non | oui |
| Polices | Google Fonts | polices système |

## Licence

[MIT](LICENSE), comme le projet d'origine (© ses auteurs). Les marques appartiennent à leurs propriétaires.

## Sur téléphone (sans PC)

Pour des proches sans ordinateur, un connecteur Garmin hébergé est décrit (en anglais) dans
[`connector/README.md`](connector/README.md).
