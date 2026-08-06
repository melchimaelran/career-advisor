# Requirements — 001 Fondations

## Vue d'ensemble

Mettre en place la structure complète et fonctionnelle du projet career-advisor :
fichiers de définition des agents, squelette des dossiers de données, règles
d'arrêt, et placeholders des skills. Cette spec est le socle sur lequel toutes
les specs suivantes (002–010) s'appuient.

---

## User stories

**US-1 — Définitions des agents**
En tant qu'Orchestrator, je dois pouvoir lire la définition de chaque agent
(rôle, inputs, outputs, contraintes) dans `agents/<nom>.md` pour savoir comment
l'invoquer et ce qu'il me retourne.

*Critères d'acceptation :*
- Les 6 fichiers existent : `orchestrator.md`, `researcher.md`,
  `knowledge-builder.md`, `interviewer.md`, `strategist.md`, `critic.md`
- Chaque fichier décrit : rôle, contexte reçu en entrée, sortie attendue,
  contraintes spécifiques à l'agent

**US-2 — Squelette knowledge/**
En tant que Knowledge Builder, je dois disposer de fichiers cibles préexistants
(avec en-têtes et format définis) pour y écrire sans avoir à les créer moi-même.

*Critères d'acceptation :*
- `knowledge/market-trends.md` existe avec en-tête de format (objectif visé,
  stack, date, source obligatoires par entrée)
- `knowledge/job-postings-analysis.md` existe avec en-tête de format
- `knowledge/sources-log.md` existe avec en-tête de format
- `knowledge/raw/` existe (dossier de cache des sources brutes)

**US-3 — Squelette memory/**
En tant qu'Interviewer, je dois disposer d'un `memory/user-profile.md` avec
un template vide pour y écrire le profil structuré de l'utilisateur après
l'entretien.

*Critères d'acceptation :*
- `memory/user-profile.md` existe avec template vide (sections pré-remplies)
- `memory/diagnostic-history.md` existe (log des runs passés, vide au départ)

**US-4 — Règle d'arrêt**
En tant que Researcher, je dois avoir une règle d'arrêt qualitative explicite
pour savoir quand m'arrêter sans avoir épuisé le sujet.

*Critères d'acceptation :*
- `rules/stopping-criteria.md` existe et décrit la règle du Researcher
  (consensus clair + principales contradictions identifiées = stop)

**US-5 — Placeholders skills/**
En tant que développeur du projet, je dois avoir une arborescence `skills/`
avec un README par sous-dossier décrivant ce que le skill doit faire, pour
orienter le travail des specs 002 et 003.

*Critères d'acceptation :*
- `skills/youtube-research/README.md` existe (description du skill, voir PRD 11.1)
- `skills/job-postings-research/README.md` existe (description, voir PRD 11.2)
- `skills/action-plan-builder/README.md` existe (template rapport, voir PRD 11.3)

---

## Exigences fonctionnelles

### P0 — Bloquant

| ID | Exigence |
|---|---|
| F-01 | Les 6 fichiers `agents/*.md` existent avec contenu réel (pas juste un placeholder vide) |
| F-02 | `knowledge/market-trends.md` définit le format d'entrée obligatoire (objectif, stack, date, source, URL) |
| F-03 | `memory/user-profile.md` contient un template vide avec toutes les sections attendues par l'Interviewer |
| F-04 | `rules/stopping-criteria.md` décrit explicitement la règle d'arrêt qualitative du Researcher |

### P1 — Important

| ID | Exigence |
|---|---|
| F-05 | `knowledge/sources-log.md` a un format de log clair (date, source, erreur éventuelle) pour la règle de repli |
| F-06 | Les READMEs des skills donnent assez de contexte pour démarrer les specs 002/003 sans relire le PRD |
| F-07 | `knowledge/raw/` est listé dans `.gitignore` (pas de cache en prod) |

### P2 — Optionnel

| ID | Exigence |
|---|---|
| F-08 | `memory/diagnostic-history.md` a un format de log horodaté (une ligne par run) |

---

## Exigences non fonctionnelles

- **Format** : Markdown uniquement, pas de scripts, pas de code Python à ce stade
- **Langue** : tout en français (contenu des fichiers), sauf les noms de fichiers
  et commandes shell
- **Cohérence** : les définitions des agents dans `agents/` doivent être cohérentes
  avec le PRD sections 4, 11.4, 11.5 — pas de réinvention

---

## Contraintes & hypothèses

- Les skills réels (code Python, etc.) sont hors périmètre de cette spec
- `CLAUDE.md` et `PRD.md` sont déjà écrits et ne font pas partie du livrable
- La spec 001 ne produit aucun code exécutable — uniquement des fichiers Markdown

---

## Hors périmètre

- Implémentation des skills (specs 002, 003)
- Définition précise des prompts système des agents (sera affinée lors des specs 004-009)
- Tests d'intégration ou d'exécution

---

## Critères de succès

- `find agents/ knowledge/ memory/ rules/ skills/ -name "*.md" | wc -l` ≥ 15
- Chaque fichier agent peut être lu par un futur agent sans avoir à relire le PRD
- Un nouveau collaborateur peut comprendre la structure du projet en lisant
  uniquement les fichiers produits par cette spec
