---
description: Pense-bête — comment utiliser le conseiller carrière tech
---

Affiche ce pense-bête à l'utilisateur, en français, sans l'exécuter comme une
tâche — c'est de l'information, pas une action :

---

**Conseiller Carrière Tech** — outil personnel, déclenchement manuel
uniquement (pas de cron, pas de scheduler).

**Lancer un diagnostic complet :** `/diagnostic`
Enchaîne automatiquement : un entretien (questions sur ta situation,
objectifs, contraintes), une recherche marché (web, Hacker News, YouTube,
offres d'emploi), une consolidation de cette recherche, un rapport de
diagnostic + plan d'action 30/90/365 jours, et une relecture qualité avant
de te le montrer. Ça prend un moment (l'entretien seul peut durer plusieurs
échanges) — relance-le quand tu veux un diagnostic à jour, ou quand ta
situation/tes objectifs ont changé.

**Où trouver tes rapports :** deux fichiers par jour de run —
`outputs/report-YYYY-MM-DD.md` (rapport tracé, sourcé dans `knowledge/`) et
`outputs/analyse-modele-YYYY-MM-DD.md` (second avis basé sur le jugement du
modèle, complémentaire, non sourcé). L'historique de tous tes runs est dans
`memory/diagnostic-history.md`.

**Repartir de zéro :** `/reset` — efface ton profil et la connaissance marché
accumulée (demande confirmation avant d'agir, garde tes rapports passés).

**Reprendre le développement de l'outil lui-même** (pas un diagnostic, le
projet Claude Code) : voir `PRD.md` section 12 (Roadmap) et `README.md`.

---
