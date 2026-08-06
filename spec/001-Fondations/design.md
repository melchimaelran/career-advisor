# Design — 001 Fondations

## Vue d'ensemble

Cette spec ne produit pas de code — uniquement des fichiers Markdown. Le
"design" décrit le contenu précis de chaque fichier à créer : structure,
sections obligatoires, format des données.

---

## Arborescence cible

```
career-advisor/
├── agents/
│   ├── orchestrator.md       ← définition de l'Orchestrator
│   ├── researcher.md         ← définition du Researcher
│   ├── knowledge-builder.md  ← définition du Knowledge Builder
│   ├── interviewer.md        ← définition de l'Interviewer
│   ├── strategist.md         ← définition du Strategist
│   └── critic.md             ← définition du Critic
├── knowledge/
│   ├── market-trends.md      ← tendances marché (format défini)
│   ├── job-postings-analysis.md  ← analyse offres d'emploi
│   ├── sources-log.md        ← log des sources/erreurs
│   └── raw/                  ← cache sources brutes (gitignored)
├── memory/
│   ├── user-profile.md       ← profil utilisateur (template)
│   └── diagnostic-history.md ← historique des runs
├── rules/
│   └── stopping-criteria.md  ← règle d'arrêt du Researcher
└── skills/
    ├── youtube-research/
    │   └── README.md         ← spec du skill YouTube
    ├── job-postings-research/
    │   └── README.md         ← spec du skill offres d'emploi
    └── action-plan-builder/
        └── README.md         ← template rapport final
```

---

## Design des fichiers agents/

### Structure commune à chaque fichier agent

```markdown
# Agent : <Nom>

## Rôle
<Une phrase — ce que l'agent fait dans le workflow>

## Position dans le workflow
<Qui l'appelle, qui il appelle ensuite>

## Contexte reçu en entrée
<Liste des informations que l'Orchestrator lui transmet>

## Sortie attendue
<Format exact de ce que l'agent retourne à l'Orchestrator>

## Contraintes
<Règles spécifiques à cet agent>

## Fichiers lus / écrits
<Liste des fichiers que l'agent lit ou écrit>
```

### Contenu spécifique par agent

**orchestrator.md** — pilote le workflow séquentiel, invoque chaque agent via
Task tool, ne garde que les résumés entre agents, écrit rien dans knowledge/.

**researcher.md** — recherche web (WebSearch/WebFetch), HN (API Algolia),
YouTube (skill 002), offres d'emploi (skill 003). S'arrête selon
`rules/stopping-criteria.md`. Applique la règle de repli si une source échoue.
Écrit dans `knowledge/raw/`. Sortie : résumé condensé pour le Knowledge Builder.

**knowledge-builder.md** — prend la sortie brute du Researcher, structure dans
`knowledge/market-trends.md` et `knowledge/job-postings-analysis.md` avec le
format obligatoire (objectif, stack, date, source, URL). Vérifie la fraîcheur
(règle 2-4 semaines). Sortie : confirmation + liste des fichiers mis à jour.

**interviewer.md** — 4 phases socratiques (faits rapides → objectifs déclarés
→ creusement → contraintes réelles). Adaptatif, sans limite de questions fixe.
Écrit dans `memory/user-profile.md` et `memory/diagnostic-history.md`.
Sortie : profil utilisateur structuré.

**strategist.md** — compare `memory/user-profile.md` vs données dans
`knowledge/`. Produit le rapport dans `outputs/` via le template
`skills/action-plan-builder/`. Sortie : chemin du rapport généré.

**critic.md** — lit le rapport généré par le Strategist. Vérifie :
concrétude (pas de recommandations vagues), cohérence avec contraintes
réelles (phase 4 de l'Interviewer), absence de contradictions entre sources.
Retourne au Strategist si trop générique. Sortie : rapport approuvé ou
liste de points à corriger.

---

## Design des fichiers knowledge/

### `knowledge/market-trends.md`

```markdown
# Tendances marché tech

<!-- Format obligatoire par entrée :
- Objectif visé : [CDI | Freelance | Remote international | Produit | Consulting]
- Stack : [liste des technos concernées]
- Date de récupération : YYYY-MM-DD
- Source : [titre de l'article/vidéo/post]
- URL : [url complète]
-->

## [Titre de l'entrée] — YYYY-MM-DD

**Objectif visé :** ...
**Stack :** ...
**Source :** [titre](url) — récupéré le YYYY-MM-DD

[Résumé de la tendance, 3-10 lignes]
```

### `knowledge/job-postings-analysis.md`

```markdown
# Analyse des offres d'emploi

<!-- Format obligatoire par batch :
- Objectif visé : ...
- Stack cible : ...
- Date d'analyse : YYYY-MM-DD
- Nombre d'offres analysées : N
- Sources : [plateformes scrapées]
-->

## Batch YYYY-MM-DD — [Objectif] / [Stack]

**Offres analysées :** N
**Sources :** ...

### Compétences les plus demandées
...

### Fourchettes salariales observées
...

### Patterns notables
...
```

### `knowledge/sources-log.md`

```markdown
# Log des sources

| Date | Source | Statut | Détail |
|------|--------|--------|--------|
| YYYY-MM-DD | youtube-research | OK | 3 vidéos récupérées |
| YYYY-MM-DD | job-postings-research | ERREUR | Structure Indeed modifiée — repli activé |
```

---

## Design des fichiers memory/

### `memory/user-profile.md`

```markdown
# Profil utilisateur

*Mis à jour le : [date du dernier run de l'Interviewer]*

## Situation actuelle
- **Métier :** ...
- **Niveau :** [Junior | Confirmé | Senior]
- **Années d'expérience :** ...
- **Stack principale :** ...
- **Type de contrat actuel :** [CDI | Freelance | Sans emploi | ...]
- **Secteur :** ...

## Objectifs déclarés
- **Type de poste visé :** [CDI | Freelance | Remote international | Produit | Consulting]
- **Horizon temporel :** ...
- **Critères prioritaires :** ...

## Tensions identifiées (phase socratique)
*(objectifs déclarés vs réalité — rempli par l'Interviewer)*
- ...

## Contraintes réelles
- **Temps disponible pour se former :** ...
- **Tolérance au risque financier :** [Faible | Moyenne | Élevée]
- **Contraintes personnelles :** ...

## Compétences actuelles
### Maîtrisées
- ...

### En cours d'apprentissage
- ...

### Identifiées comme manquantes (auto-évaluation)
- ...
```

### `memory/diagnostic-history.md`

```markdown
# Historique des diagnostics

| Date | Objectif visé | Stack | Rapport généré |
|------|--------------|-------|----------------|
| YYYY-MM-DD | ... | ... | outputs/report-YYYY-MM-DD.md |
```

---

## Design des fichiers rules/

### `rules/stopping-criteria.md`

Contenu : définition de la règle d'arrêt qualitative du Researcher :
- Arrêt quand consensus clair sur au moins 3 sources indépendantes ET
  principales contradictions identifiées (pas quand le sujet est épuisé)
- Critères spécifiques par type de source (web, HN, YouTube, offres)
- Comportement si une source échoue (règle de repli : continuer, logger)

---

## Design des fichiers skills/ READMEs

Chaque README décrit : objectif du skill, dépendances techniques, inputs
attendus, outputs produits, comportement de repli si applicable.

**`skills/youtube-research/README.md`** — adapté de zerowing113/claude-youtube-skill.
Recherche par mot-clé via yt-dlp, fetch transcripts (priorité français), vérification
cache avant fetch, sortie Markdown horodatée dans `knowledge/raw/`.

**`skills/job-postings-research/README.md`** — basé sur python-jobspy. Inputs :
poste, stack, localisation, nb d'offres. Outputs : liste d'offres en JSON/Markdown
dans `knowledge/raw/`. Règle de repli obligatoire (log erreur + continuer).

**`skills/action-plan-builder/README.md`** — template du rapport final. Décrit
les 5 sections obligatoires : résumé diagnostic, forces/faiblesses/manques/
avantages/blocages/opportunités, plan 30j, plan 90j, plan 365j. Chaque action
doit avoir un critère de "fait" vérifiable.

---

## .gitignore

Ajouter `knowledge/raw/` au `.gitignore` (cache de sources brutes, potentiellement
volumineux et inutile à versionner).

---

## Risques techniques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Définitions agents trop vagues → Orchestrator ne sait pas comment les invoquer | Moyenne | Haut | Sections "Contexte reçu" et "Sortie attendue" précises et testables |
| Format knowledge/ non respecté par le Knowledge Builder | Faible | Moyen | Commentaires de format dans chaque fichier (visibles même si le fichier est vide) |
| Redondance entre agents/*.md et PRD.md | Haute | Faible | agents/*.md sont la source de vérité opérationnelle — le PRD explique le "pourquoi" |
