# Conseiller Carrière Tech — outil personnel

Pipeline multi-agent [Claude Code](https://claude.com/claude-code) qui produit un
diagnostic carrière personnalisé pour un développeur : entretien socratique →
recherche du marché de l'emploi tech ciblée sur le profil → rapport + plan
d'action 30/90/365 jours, relu pour qu'il soit vraiment exploitable.

Outil **strictement personnel** — pas de SaaS, pas de frontend, pas de serveur,
déclenchement manuel. Le repo est public comme **référence d'architecture**
Claude Code.

**Statut** : les 6 agents et les 3 skills sont implémentés et ont tourné au moins
une fois (`outputs/` du 2026-08-06). Le test end-to-end formel du workflow complet
reste à faire (`PRD.md` §12).

## Ce qui peut servir de référence

- **Sous-agents à contexte isolé** — le Researcher produit un gros volume brut
  (transcripts, offres d'emploi). En subagents `Task` isolés, ce bruit ne remonte
  jamais aux agents suivants : seul le résumé condensé transite. Moins cher en
  tokens, contexte plus propre.
- **Contournement d'une limite plateforme** — `AskUserQuestion` est indisponible
  dans les subagents Claude Code. Les deux agents qui dialoguent avec l'utilisateur
  (Orchestrator, Interviewer) tournent donc en **main thread** : l'Orchestrator est
  une slash command (`.claude/commands/diagnostic.md`), pas un subagent.
- **Un subagent qui ne peut pas écrire son livrable** — le Strategist a `Write`
  bloqué (fichiers de type « rapport ») ; il retourne le texte, et l'Orchestrator
  persiste les fichiers `outputs/`. Contrainte plateforme documentée, pas un bug.
- **Persistance 100 % fichiers** — Markdown principalement, JSON pour les données
  structurées (offres d'emploi). Aucune base de données : le volume d'un usage
  perso ne justifie pas SQLite.
- **Critère d'arrêt qualitatif** — le Researcher s'arrête quand il a un consensus
  clair + les contradictions principales, pas quand il a épuisé le sujet. Détail :
  `rules/stopping-criteria.md`.
- **Règle de repli sur sources fragiles** — si le scraping d'offres casse, le
  Researcher continue avec les autres sources et logue l'échec dans
  `knowledge/sources-log.md`.
- **Règle de fraîcheur** — données de `knowledge/` réutilisées si moins de ~2-4 semaines
  et profil inchangé, sinon recherche neuve.
- **Un seul Critic**, pas de debate/adversarial, pas de recursive improvement, pas
  de knowledge graph — gain marginal pour un outil solo, complexité réelle.

Justification complète de chaque choix : `PRD.md`. Contrats détaillés des agents :
`agents/*.md` (les 4 subagents `Task` sont enregistrés comme stubs dans
`.claude/agents/` qui délèguent à ces contrats).

## Ce que ça fait

| Étape | Contenu |
|---|---|
| **Entrée** | Une conversation : métier actuel, niveau, stack, objectifs (CDI, freelance, remote international, produit, consulting), contraintes réelles. |
| **Traitement** | Entretien adaptatif → recherche marché ciblée (web, Hacker News, YouTube, offres d'emploi) → base de connaissance datée et sourcée → analyse comparative profil actuel vs profil cible du marché. |
| **Sortie** | `outputs/report-YYYY-MM-DD.md` — diagnostic (forces / faiblesses / compétences manquantes / avantages compétitifs / blocages / opportunités) + plans 30/90/365 jours, chaque action avec un critère de « fait » vérifiable. |
| **Sortie bis** | `outputs/analyse-modele-YYYY-MM-DD.md` — un second avis basé sur le jugement général du modèle, complémentaire au rapport, **non sourcé** et non relu par le Critic (avertissement en tête de fichier). |

Un clone démarre vide : `memory/`, `knowledge/raw/` et les fichiers générés de
`knowledge/` + `outputs/` sont gitignorés (seuls les `README.md` de ces dossiers
sont suivis). Tout se génère localement avec `/diagnostic`.

## Workflow

```
/diagnostic  =  Orchestrator (slash command, main thread)
     │
     ├─▶ Interviewer        entretien socratique 4 phases   ·  main thread
     │        └─ écrit  memory/user-profile.md
     │
     ├─▶ Researcher         web / HN / YouTube / offres      ·  Task subagent
     │        └─ écrit  knowledge/raw/
     │
     ├─▶ Knowledge Builder  structure les trouvailles brutes ·  Task subagent
     │        └─ écrit  knowledge/market-trends.md, job-postings-analysis.md
     │
     ├─▶ Strategist         compare profil vs marché         ·  Task subagent
     │        └─ retourne le texte du rapport + de l'analyse (Write bloqué)
     │
     ├─▶ Critic             concret ? personnalisé ? tracé ?  ·  Task subagent
     │        └─ renvoie au Strategist si générique
     │
     └─▶ Orchestrator       écrit outputs/report-*.md + analyse-modele-*.md
```

L'Interviewer passe **en premier** : coût quasi nul, et connaître le profil avant
la recherche évite au Researcher une recherche marché générique.

## Utiliser l'outil

Ouvrir ce dossier dans Claude Code, puis :

- **`/diagnostic`** — run complet. Relancer quand la situation change.
- **`/aide`** — pense-bête rapide.
- **`/reset`** — efface profil + connaissance marché (demande confirmation, garde
  les rapports passés dans `outputs/`).

### Prérequis

- **Claude Code** (les agents, skills et slash commands sont des fichiers
  `.claude/` + `agents/` + `skills/`).
- **Python 3** pour 2 skills : `youtube-research` (yt-dlp,
  youtube-transcript-api) et `job-postings-research` (python-jobspy). Chaque skill
  gère son propre `.venv` — voir `skills/<nom>/`. Le 3ᵉ skill,
  `action-plan-builder`, est un simple template Markdown.
- Exécution locale (testé sous Ubuntu). Aucune clé API tierce : Hacker News passe
  par l'API Algolia gratuite, le reste par la recherche web native de Claude Code.
- Le scraping d'offres d'emploi n'est pas officiel et peut casser si les
  plateformes changent de structure (voir « Règle de repli » ci-dessus).

## Structure

```
agents/     contrats détaillés des 6 agents
skills/     2 scripts Python (youtube-research, job-postings-research) + 1 template (action-plan-builder)
rules/      règles opérationnelles référencées par les agents (ex: critère d'arrêt)
knowledge/  connaissance marché persistante — contenu gitignoré, alimenté par Researcher + Knowledge Builder
memory/     profil utilisateur + historique des runs — gitignoré, alimenté par l'Interviewer
outputs/    rapports générés — gitignorés (seul outputs/README.md est suivi)
.claude/    commands/ (diagnostic, aide, reset) + agents/ (stubs des 4 subagents Task)
```

## Pour le mainteneur

Reprendre le développement : ouvrir ce dossier dans Claude Code, lire `PRD.md`
§12 (Roadmap) pour identifier l'étape en cours, puis `/plan` pour la suivante.
Historique des runs : `memory/diagnostic-history.md`.

## Licence

MIT — voir `LICENSE`.
