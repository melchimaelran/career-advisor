# Tasks — 001 Fondations

## Vue d'ensemble

Création de ~15 fichiers Markdown. Aucun code. Durée estimée : 1 session.
Toutes les tâches sont indépendantes sauf T-16 (.gitignore) qui dépend de T-11.

---

## Phase 1 — Agents (F-01)

- [x] T-01 : Créer `agents/orchestrator.md` avec rôle, position workflow, contexte reçu, sortie attendue, contraintes, fichiers lus/écrits
- [x] T-02 : Créer `agents/researcher.md` — inclure référence à `rules/stopping-criteria.md` et règle de repli
- [x] T-03 : Créer `agents/knowledge-builder.md` — inclure référence au format `knowledge/market-trends.md`
- [x] T-04 : Créer `agents/interviewer.md` — décrire les 4 phases socratiques et les fichiers memory/ écrits
- [x] T-05 : Créer `agents/strategist.md` — référencer `skills/action-plan-builder/`
- [x] T-06 : Créer `agents/critic.md` — décrire la checklist de relecture (3 critères du PRD 11.5)

## Phase 2 — Knowledge (F-02, F-05)

- [x] T-07 : Créer `knowledge/market-trends.md` avec en-tête de format commenté (objectif, stack, date, source, URL obligatoires)
- [x] T-08 : Créer `knowledge/job-postings-analysis.md` avec en-tête de format commenté
- [x] T-09 : Créer `knowledge/sources-log.md` avec tableau vide (Date | Source | Statut | Détail)
- [x] T-10 : Créer `knowledge/raw/.gitkeep` (dossier de cache, doit exister mais rester vide en git)

## Phase 3 — Memory (F-03, F-08)

- [x] T-11 : Créer `memory/user-profile.md` avec template complet (7 sections : situation actuelle, objectifs déclarés, tensions, contraintes réelles, compétences maîtrisées, en cours, manquantes)
- [x] T-12 : Créer `memory/diagnostic-history.md` avec tableau vide (Date | Objectif | Stack | Rapport)

## Phase 4 — Rules (F-04)

- [x] T-13 : Créer `rules/stopping-criteria.md` — règle d'arrêt qualitative du Researcher + comportement de repli par type de source

## Phase 5 — Skills READMEs (F-06)

- [x] T-14 : Créer `skills/youtube-research/README.md` — objectif, dépendances (yt-dlp, youtube-transcript-api), inputs, outputs, cache, comportement repli
- [x] T-15 : Créer `skills/job-postings-research/README.md` — objectif, dépendances (python-jobspy), inputs, outputs, règle de repli obligatoire
- [x] T-16 : Créer `skills/action-plan-builder/README.md` — template 5 sections rapport final avec critères de "fait" vérifiables

## Phase 6 — Config (F-07)

- [x] T-17 : Ajouter `knowledge/raw/` au `.gitignore`

---

## Critères de validation (Definition of Done)

Chaque tâche est cochée `[x]` uniquement si :
1. Le fichier existe à l'emplacement exact spécifié
2. Le contenu est réel (pas un placeholder vide)
3. Il est cohérent avec le PRD (sections 4, 11.x correspondantes)

Vérification finale :
```bash
find agents/ knowledge/ memory/ rules/ skills/ -name "*.md" | wc -l
# Résultat attendu : ≥ 15
```
