# Conseiller Carrière Tech — outil personnel

Outil personnel basé sur Claude Code. Vision complète et décisions : PRD.md.
Contexte chargé automatiquement par Claude Code à chaque session : CLAUDE.md.

Partagé en public comme référence d'architecture (6 agents Claude Code + skills
Python). Les données produites à l'usage — `memory/`, `knowledge/`, `outputs/*.md`
— sont gitignorées : un clone démarre vide, sans profil ni rapport. Lancer
`/diagnostic` pour tout générer localement.

## Utiliser l'outil

Ouvrir ce dossier dans Claude Code, puis :

- **`/diagnostic`** — lance un run complet (entretien → recherche marché →
  consolidation → rapport de diagnostic + plan d'action 30/90/365 jours →
  relecture qualité). Déclenchement manuel uniquement, pas de cron — relance
  quand tu veux un diagnostic à jour ou que ta situation a changé.
- **`/aide`** — pense-bête rapide si tu reviens sans contexte.
- **`/reset`** — efface profil + connaissance marché pour repartir de zéro
  (demande confirmation, garde les rapports passés dans `outputs/`).

Chaque run produit deux fichiers : `outputs/report-YYYY-MM-DD.md` (rapport
tracé, sources dans `knowledge/`) et `outputs/analyse-modele-YYYY-MM-DD.md`
(second avis basé sur le jugement du modèle, complémentaire, non sourcé).
Historique des runs dans `memory/diagnostic-history.md`.

## Pour reprendre le développement de l'outil lui-même

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
