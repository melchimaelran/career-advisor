# CLAUDE.md — Conseiller Carrière Tech (projet personnel)

## Contexte

Outil personnel d'IA (pas un SaaS, pas de frontend, pas de VPS) qui construit une
connaissance du marché de l'emploi tech et produit, pour l'utilisateur (développeur
~5 ans d'XP), un diagnostic personnalisé + une analyse comparative + un plan d'action
concret sur 30/90/365 jours.

Vision complète, décisions et justifications : voir `PRD.md`.

## Langue de communication

Claude répond **toujours en français** dans ce projet — conversations, explications,
questions de clarification, résumés. Seuls les blocs de code et les commandes
shell restent en anglais.

## Contraintes globales — ne jamais dévier

- Usage strictement personnel. Pas d'adaptation multi-domaine pour l'instant.
- Déclenchement **manuel uniquement**. Pas de cron, pas de scheduler, pas de VPS.
- Stockage : **fichiers Markdown** (+ JSON si besoin de données structurées).
  Pas de SQLite, pas de base de données.
- Éviter la complexité inutile : **pas** de debate/adversarial agents, **pas** de
  recursive improvement, **pas** de knowledge graph. Un seul Critic pour la relecture.
- Sortie toujours en français.
- Pas de budget de recherche chiffré, mais un **critère d'arrêt qualitatif** : le
  Researcher s'arrête quand il a identifié un consensus clair et les principales
  contradictions — pas quand il a épuisé le sujet.

## Architecture — 6 agents

Chaque agent est un **vrai subagent Claude Code** (contexte isolé, invoqué via Task),
pas un simple changement de "rôle" dans une conversation continue. Raison : le
Researcher notamment produit un gros volume de contenu brut (transcripts, offres
d'emploi) qui ne doit jamais polluer le contexte des agents suivants.

1. **Orchestrator** — pilote le workflow, ne garde que les résumés/handoffs entre agents
2. **Researcher** — recherche web, Hacker News, YouTube, offres d'emploi
3. **Knowledge Builder** — structure les trouvailles dans `knowledge/`
4. **Interviewer** — entretien socratique, adaptatif, sans limite de questions fixe
5. **Strategist** — analyse comparative (profil actuel vs marché) + plan d'action
6. **Critic** — relit le rapport final avant livraison, vérifie qu'il est vraiment
   exploitable et pas générique

Définitions détaillées de chaque agent : `agents/<nom>.md`.

## Workflow d'exécution

```
Interviewer → Researcher → Knowledge Builder → Strategist → Critic
```

L'Interviewer passe **en premier** : ça permet au Researcher de cibler sa recherche
sur le profil réel de l'utilisateur au lieu de partir sur une recherche générique
(économie de tokens, pertinence accrue).

## Règle de fraîcheur des données

Avant de relancer une recherche, le Researcher compare le profil/objectif actuel
(sortie de l'Interviewer) au dernier profil stocké dans `memory/user-profile.md` :

- **Même objectif/profil** → réutiliser les données de `knowledge/` si elles ont
  moins de ~2-4 semaines
- **Objectif ou profil différent** → recherche ciblée neuve, peu importe l'âge des
  données précédentes

Chaque entrée de `knowledge/market-trends.md` doit indiquer : objectif visé, stack,
et date — pas de blob générique de "tendances marché".

## Règle de repli (résilience des sources)

Si une source échoue (ex: le scraping d'offres d'emploi casse parce que le site a
changé de structure), le Researcher **continue avec les autres sources** plutôt que
de bloquer tout le run, et log l'échec dans `knowledge/sources-log.md` pour que
l'utilisateur sache qu'il faut vérifier/mettre à jour l'outil concerné.

## Sources du Researcher

| Source | Méthode | Statut |
|---|---|---|
| Blogs / articles / rapports | Recherche web native (WebSearch/WebFetch) | Facile, fiable |
| Hacker News | API Algolia (appel HTTP direct, pas de clé) | Facile, fiable |
| YouTube | `skills/youtube-research/` (yt-dlp + youtube-transcript-api) | Adapté d'un repo existant |
| Offres d'emploi | `skills/job-postings-research/` (python-jobspy) | Fragile — scraping non officiel, prévoir repli |
| Reddit | Recherche web (threads remontent naturellement) | Pas de scraping direct |
| Discord (communautés francophones) | Apport manuel de l'utilisateur | Non automatisé |

## Règle de citation

Toute donnée écrite dans `knowledge/` doit être **datée et sourcée** (titre, URL,
date de récupération). Jamais d'affirmation sans origine traçable.

## Livrable final

Un rapport Markdown dans `outputs/`, structuré ainsi (template complet :
`skills/action-plan-builder/`) :
1. Résumé du diagnostic (profil actuel vs profil cible marché)
2. Forces / faiblesses / compétences manquantes / avantages compétitifs / blocages / opportunités
3. Plan d'action 30 jours (actions concrètes, critère de "fait" vérifiable)
4. Plan d'action 90 jours
5. Plan d'action 365 jours

## Méthode d'implémentation

Ce projet est construit avec un workflow **Spec-Driven Development** : commandes
`/spec:*` dans `.claude/commands/spec/`, reprises **sans modification** de
https://github.com/papaoloba/spec-based-claude-code.

- Spec active : voir `spec/.current-spec`
- Roadmap complète des specs : `PRD.md`, section "Roadmap d'implémentation"
- Pour reprendre le travail à tout moment : lancer `/spec:status`

Une tâche n'est cochée `[x]` dans `tasks.md` que si : le code fonctionne, a été
testé manuellement (exécution réelle, pas supposée), et produit une sortie conforme
aux critères d'acceptation de la spec. Si le test échoue : corriger, retester,
reboucler jusqu'à validation — ne jamais cocher une tâche "probablement" bonne.
