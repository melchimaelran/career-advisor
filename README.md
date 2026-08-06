# Conseiller Carrière Tech — outil personnel

Outil personnel basé sur Claude Code. Vision complète et décisions : PRD.md.
Contexte chargé automatiquement par Claude Code à chaque session : CLAUDE.md.

## Pour reprendre le travail

Ouvrir ce dossier dans Claude Code, lire `PRD.md` section 12 (Roadmap) pour
identifier l'étape en cours, puis demander à Claude de planifier la prochaine étape.

## Architecture

6 agents Claude Code (contexte isolé via Task) : Orchestrator → Interviewer →
Researcher → Knowledge Builder → Strategist → Critic. Détails : `agents/<nom>.md`.

## Structure

```
agents/     définitions des 6 agents
skills/     scripts Python réutilisables (youtube-research, job-postings-research, action-plan-builder)
knowledge/  connaissance marché persistante (alimentée par Researcher + Knowledge Builder)
memory/     profil utilisateur + historique (alimentés par Interviewer)
rules/      règles opérationnelles référencées par les agents
outputs/    rapports finaux générés (report-YYYY-MM-DD.md)
```
