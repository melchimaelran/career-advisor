# Règle d'arrêt du Researcher

## Principe

Le Researcher s'arrête quand il a identifié **un consensus clair** et les
**principales contradictions** — pas quand il a épuisé le sujet.

L'objectif est la pertinence, pas l'exhaustivité.

## Critère d'arrêt qualitatif

Le Researcher peut s'arrêter quand **les trois conditions suivantes sont remplies** :

1. **Consensus identifié** : au moins 3 sources indépendantes convergent sur les
   mêmes tendances ou compétences pour le profil ciblé
2. **Contradictions cartographiées** : les points de désaccord entre sources sont
   identifiés et notés (ex: "Source A dit X est requis, Source B dit X est dépassé")
3. **Couverture des sources principales** : au moins 2 types de sources différents
   ont été consultés parmi [web, HN, YouTube, offres d'emploi]

## Ce qui ne déclenche PAS l'arrêt

- Avoir lu un nombre fixe d'articles (pas de quota)
- Avoir épuisé toutes les sources disponibles
- Ne plus trouver de nouvelles informations (ce n'est pas le critère — le critère
  est d'avoir assez pour un diagnostic utile)

## Comportement si une source échoue (règle de repli)

| Situation | Action |
|-----------|--------|
| Source inaccessible (timeout, erreur HTTP) | Continuer avec les autres sources |
| Skill cassé (scraping offres, YouTube) | Continuer sans ce skill |
| Aucune source ne fonctionne | Stopper le run, signaler à l'Orchestrator |

Dans tous les cas d'échec : logger dans `knowledge/sources-log.md` (date,
source, statut ERREUR, détail de l'erreur).

## Critère d'arrêt par type de source

| Source | Arrêt quand... |
|--------|---------------|
| Web (articles) | 5-10 articles pertinents lus et résumés |
| Hacker News | 1 recherche par mot-clé principal, top 10 résultats parcourus |
| YouTube | 2-4 vidéos pertinentes transcrites |
| Offres d'emploi | 30-50 offres analysées (ou moins si peu disponibles) |
