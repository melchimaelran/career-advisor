# PRD — Conseiller Carrière Tech (Outil Personnel IA)

Document de référence complet. `CLAUDE.md` en est le résumé opérationnel chargé à
chaque session Claude Code ; ce document explique le "pourquoi" derrière chaque
décision.

---

## 1. Vision & contexte

Construire un outil personnel (pas un SaaS) basé sur Claude Code qui fonctionne comme
un "AI Operating System" pour un premier cas d'usage concret : un conseiller
stratégique carrière pour les métiers tech.

Le système doit :
1. Construire une connaissance à jour du marché de l'emploi tech (compétences
   recherchées, différences junior/confirmé/senior, CDI/freelance/entrepreneuriat,
   impact de l'IA sur les métiers)
2. Faire un diagnostic personnalisé de l'utilisateur via une approche socratique
3. Produire une analyse stratégique comparant profil actuel vs profil idéal du
   marché, avec un plan d'action concret

## 2. Contraintes & périmètre

- Outil personnel, pas de réutilisation multi-domaine planifiée dès le départ
  (on pourra extraire des patterns réutilisables *après* avoir vu ce qui marche
  réellement sur ce premier cas d'usage — pas avant)
- Pas de frontend, pas de VPS, pas de déploiement serveur : exécution locale sur
  poste Ubuntu, déclenchement manuel uniquement
- Stockage fichiers (Markdown/JSON), pas de base de données
- Priorité à un système "équilibré" : ni minimal, ni maximal — puissant mais
  maintenable par une seule personne

## 3. Cas d'usage

L'utilisateur décrit son métier actuel, son niveau, son expérience, ses compétences,
et ses objectifs (CDI, freelance, remote international, création de produit,
consulting). Le système pose des questions socratiques pour clarifier au-delà des
réponses de surface, recherche l'état réel du marché pour ce profil précis, puis
produit un diagnostic comparatif et un plan d'action.

## 4. Architecture des agents

6 agents, chacun un **vrai subagent Claude Code** (Task tool, contexte isolé) :

| Agent | Rôle |
|---|---|
| **Orchestrator** | Pilote le workflow, ne garde que les résumés/handoffs entre agents |
| **Researcher** | Recherche web, HN, YouTube, offres d'emploi — cible sa recherche sur le profil fourni par l'Interviewer |
| **Knowledge Builder** | Structure les trouvailles du Researcher dans `knowledge/`, gère la fraîcheur des données |
| **Interviewer** | Entretien socratique en 4 phases (faits rapides → objectifs déclarés → creusement/tensions → contraintes réelles) |
| **Strategist** | Compare profil actuel vs profil cible marché, produit le plan d'action 30/90/365j |
| **Critic** | Relit le rapport final, vérifie qu'il est concret et pas générique, vérifie la cohérence avec les contraintes réelles de l'utilisateur |

### Pourquoi des subagents et pas une conversation continue

Dans un contexte unique, tout contenu brut lu par le Researcher (transcripts,
offres d'emploi, articles) reste dans l'historique et est refacturé à chaque tour
suivant, même pour les agents qui n'en ont plus besoin. Avec des subagents isolés,
ce "bruit" ne remonte jamais en amont — seul le résultat condensé est transmis à
l'Orchestrator. C'est structurellement moins coûteux en tokens pour un système où
l'agent le plus lourd (Researcher) produit justement le plus de volume brut.

## 5. Patterns écartés et pourquoi

Patterns multi-agents envisagés initialement mais volontairement exclus :

- **Debate / Adversarial agents** — complexité et coût en tokens disproportionnés
  pour un outil solo ; le gain vs un Critic simple est marginal sur ce cas d'usage
- **Recursive improvement** — même logique, boucles itératives coûteuses sans
  bénéfice net démontré ici
- **Knowledge Graph** — prématuré : Markdown/JSON suffisent largement au volume de
  données d'un usage personnel ; un knowledge graph n'aurait de sens que si on
  avait besoin de requêtes relationnelles complexes, ce qui n'est pas le cas

Un seul **Critic** couvre le besoin de contrôle qualité, sans la complexité
additionnelle du debate ou du judge séparé.

## 6. Stockage & persistance

Markdown comme format principal, JSON en complément pour données structurées si
besoin (scores, dates). Pas de SQLite : le volume de données d'un usage personnel
ne justifie pas une base de données, et SQLite ne deviendrait pertinent que pour
des requêtes complexes (ex: croiser des centaines d'offres d'emploi), ce qui n'est
pas notre besoin actuel.

**Pourquoi un système de stockage est nécessaire** (et pas juste des recherches à
la volée à chaque run) :
- Sans mémoire persistante, le Researcher referait les mêmes recherches à chaque
  lancement — gaspillage de tokens
- Impossible de suivre l'évolution de l'utilisateur dans le temps sans historique
- Le système doit accumuler de la connaissance au fil des runs, pas repartir de
  zéro à chaque fois

## 7. Sources de recherche du Researcher

| Source | Méthode | Statut |
|---|---|---|
| Blogs / articles / rapports | Recherche web native | Facile, fiable |
| Hacker News | API Algolia (appel HTTP direct, gratuit, pas de clé) | Facile, fiable |
| YouTube | Skill dédié — voir section 11 | Adapté d'un repo existant, gratuit, local |
| Offres d'emploi | Skill dédié — voir section 11 | Fragile (scraping non officiel), avec repli |
| Reddit | Recherche web (threads remontent naturellement) | Pas de scraping direct (API payante depuis 2023) |
| Discord (communautés francophones : DevCord, Graven, Talent Hub) | Apport manuel de l'utilisateur | Non automatisé — pas de bot dédié |

### Sources écartées ou limitées, et pourquoi

- **LinkedIn scraping avec compte connecté** — écarté catégoriquement : l'accord
  d'utilisateur LinkedIn interdit explicitement les scripts/robots, et
  l'enforcement peut faire sauter le compte personnel de l'utilisateur. Risque
  disproportionné pour un outil perso.
- **Services de scraping payants tiers (Apify, TranscriptAPI...)** — écartés par
  défaut : on privilégie des outils gratuits et locaux (yt-dlp,
  youtube-transcript-api, python-jobspy) cohérents avec la philosophie du projet.

## 8. Workflow d'exécution

```
Interviewer → Researcher → Knowledge Builder → Strategist → Critic
```

L'Interviewer passe en premier : le coût est quasi nul (pas d'appel web), et
connaître le profil avant de lancer la recherche permet au Researcher de cibler
au lieu de partir sur une recherche marché générique — cohérent avec le critère
d'arrêt qualitatif (moins de bruit, moins de tokens gaspillés).

## 9. Communication inter-agents

Deux niveaux distincts :

- **Intra-run** : l'Orchestrator appelle chaque agent séquentiellement, lui
  transmet seulement le contexte nécessaire, récupère sa sortie condensée, la
  transmet à l'agent suivant. Pas de "discussion libre" entre agents.
- **Inter-run (persistance)** : les agents qui produisent de la connaissance
  durable écrivent dans `knowledge/` et `memory/`. Le run suivant part de cette
  base au lieu de tout refaire.

## 10. Arborescence du projet

```
career-advisor/
├── CLAUDE.md
├── PRD.md
├── agents/
│   ├── orchestrator.md
│   ├── researcher.md
│   ├── knowledge-builder.md
│   ├── interviewer.md
│   ├── strategist.md
│   └── critic.md
├── skills/
│   ├── youtube-research/
│   ├── job-postings-research/
│   └── action-plan-builder/
├── knowledge/
│   ├── market-trends.md
│   ├── job-postings-analysis.md
│   ├── sources-log.md
│   └── raw/                   # cache des sources brutes (transcripts, offres scrapées)
├── memory/
│   ├── user-profile.md
│   └── diagnostic-history.md
├── rules/
│   └── stopping-criteria.md
└── outputs/
    └── report-YYYY-MM-DD.md
```

## 11. Contenu des skills

### 11.1 `skills/youtube-research/`

Adapté du repo public `zerowing113/claude-youtube-skill` (gratuit, local, pas de
clé API : `youtube-transcript-api` + `yt-dlp`).

**Repris tel quel** : détection URL (vidéo/playlist), `fetch_metadata()`,
`fetch_transcript()`, format de sortie markdown horodaté (déjà une bonne "source
brute citable").

**Modifié** :
- Langue de transcript : ajout du français dans les langues prioritaires (le
  script d'origine priorise l'anglais par défaut)
- Ajout d'une fonction de **recherche par mot-clé** (absente du repo d'origine,
  qui ne traite que des URLs fournies) via `yt-dlp "ytsearchN:mot-clé"
  --flat-playlist`
- Ajout d'une vérification de cache avant de fetch (évite de re-traiter une vidéo
  déjà récupérée récemment)

**Écarté** : toute la logique de compilation en "article de référence" façon
Obsidian (iframe, sections thématiques, curriculum de playlist) — hors sujet pour
notre pipeline. Notre Knowledge Builder digère directement les fichiers bruts.

### 11.2 `skills/job-postings-research/`

Basé sur `python-jobspy` (gratuit, pas de connexion à un compte personnel requise,
donc pas de risque de ban de compte — contrairement aux skills LinkedIn qui
nécessitent une session connectée).

Point de vigilance à documenter dans le skill : scraping non officiel, peut casser
si les plateformes changent leur structure de page. Comportement de repli
obligatoire (voir section "Règle de repli" dans `CLAUDE.md`).

### 11.3 `skills/action-plan-builder/`

Template du rapport final (voir `CLAUDE.md`, section "Livrable final") : résumé
diagnostic, analyse en 6 catégories, plans 30/90/365 jours avec critères de "fait"
vérifiables (jamais d'action vague type "améliorer ses compétences").

### 11.4 Interviewer — flow socratique

4 phases, **adaptatif, sans limite de questions fixe** (s'arrête quand l'agent a
assez de matière, pas sur un nombre de questions prédéfini) :

1. **Faits rapides** (fermé, factuel) — métier actuel, niveau, XP, stack
2. **Objectifs déclarés** — CDI / freelance / remote international / produit / consulting
3. **Creusement socratique** — challenge les réponses de la phase 2, détecte les
   tensions entre objectifs déclarés (ex: "freelance" + "besoin de stabilité
   financière" = tension à faire remonter explicitement, pas à ignorer)
4. **Contraintes réelles** — temps disponible, tolérance au risque, situation
   personnelle contraignante, souvent différentes de ce qui est énoncé en phase 2

Sortie : `memory/user-profile.md` mis à jour + entrée ajoutée dans
`memory/diagnostic-history.md` avec la date.

### 11.5 Critic — checklist de relecture

Avant livraison, vérifie :
- Les recommandations sont-elles concrètes ou génériques ? (renvoie au Strategist
  si trop vague)
- Y a-t-il des contradictions entre les sources citées dans `knowledge/` ?
- Le plan est-il réaliste compte tenu des contraintes réelles identifiées en
  phase 4 de l'Interviewer — pas juste "un bon plan dans l'absolu", un bon plan
  *pour cette personne précise*

## 12. Roadmap d'implémentation

Implémentation par étapes en Plan mode. Ordre à respecter : skills avant le
Researcher, agents avant l'Orchestrator, Orchestrator avant le test end-to-end.

| Étape | Contenu | Difficulté | Statut |
|-------|---------|-----------|--------|
| Fondations | Structure projet, CLAUDE.md, dossiers knowledge/memory/rules/, READMEs agents/skills | 🟢 Facile | ✅ Fait |
| skill-youtube | Script Python youtube-research (voir 11.1) | 🟡 Moyen | ✅ Fait |
| skill-job-postings | Script Python job-postings-research (voir 11.2) | 🔴 Difficile | ⬜ À faire |
| agent-researcher | Agent Researcher — orchestre web/HN/skills | 🟡 Moyen | ⬜ À faire |
| agent-interviewer | Agent Interviewer — flow socratique (voir 11.4) | 🟡 Moyen | ⬜ À faire |
| agent-knowledge-builder | Agent Knowledge Builder | 🟢 Facile | ⬜ À faire |
| agent-strategist | Agent Strategist — template rapport (voir 11.3) | 🟢 Facile | ⬜ À faire |
| agent-critic | Agent Critic — checklist (voir 11.5) | 🟢 Facile | ⬜ À faire |
| agent-orchestrator | Agent Orchestrator — assemble tout, gère les subagents | 🔴 Difficile | ⬜ À faire |
| e2e-test | Test end-to-end complet du workflow | 🟡 Moyen | ⬜ À faire |
