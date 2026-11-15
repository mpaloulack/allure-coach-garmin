# Sécurité et vie privée

Ce fork traite des données de santé (FC, VFC, sommeil, douleurs signalées) et d'activité. Voici ce qu'il fait pour les protéger, et ce qui reste à ta charge.

## Choix de conception

| Risque | Dans l'original (COROS) | Dans ce fork |
|---|---|---|
| La page modifie la montre | la page peut appeler `updateTrainingPlan` | la page n'a aucun accès à Garmin ; Claude n'utilise que des outils de lecture |
| Injection HTML (XSS) via un nom d'activité, une note, une demande de plan ou un texte copié d'un site de course | texte inséré sans échappement (`innerHTML`) | tout texte est échappé à l'entrée (`clean()`), y compris les données relues dans la base |
| Fermeture de la balise `<script>` par un texte du COACH | non traité | `inject-coach.py` échappe `</` et U+2028/2029 et vérifie la syntaxe |
| Localisation du domicile | coordonnées de départ de chaque sortie, arrondies à ~1 km, stockées en base | aucune coordonnée de sortie ; une position fixe de la ville (`wxGeo`, arrondie à 0,1°) pour la météo |
| Fuite d'IP au chargement | Google Fonts | polices système, aucune ressource externe au chargement |
| Injection d'instructions dans Claude (un nom d'activité ou une note qui « donne des ordres ») avec un outil d'écriture en « Toujours autoriser » | conseillé dans le README | le guide traite ces textes comme des données, et il n'y a plus d'outil d'écriture Garmin |

## Ce qui reste à ta charge

- **Le lien du dashboard** : l'artifact est privé, mais toute personne qui a le lien voit tes données. Ne le partage pas, ne le colle pas dans une issue.
- **Le connecteur Garmin** : il a accès à tout ton compte Garmin Connect. Choisis-en un de confiance, **fige sa version** (pas de `@latest` lancé automatiquement) et garde ses jetons dans un fichier lisible par toi seul (`chmod 600`). Active la double authentification sur ton compte Garmin.
- **Les permissions** : n'autorise que les outils de lecture du connecteur ; n'en passe aucun en « Toujours autoriser » s'il peut écrire.
- **Les mises à jour du kit** : relis les changements du modèle HTML avant de le remplacer.

## Signaler un problème

Ouvre une issue sans données personnelles (ni nom, ni FC, ni position, ni lien de dashboard).
