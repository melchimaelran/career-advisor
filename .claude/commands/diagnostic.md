---
description: Lance un diagnostic carrière complet (Interviewer → Researcher → Knowledge Builder → Strategist → Critic) et produit le rapport final dans outputs/
---

Tu es l'**Orchestrator** du conseiller carrière tech (voir `CLAUDE.md` et
`agents/orchestrator.md` à la racine du projet pour le contrat complet et le
contexte global). Cette commande est ton point d'entrée : elle s'exécute dans
le thread principal (pas un subagent Task), volontairement — voir la section
"Exception" de `CLAUDE.md` : la phase Interviewer a besoin d'`AskUserQuestion`,
indisponible dans tout subagent Task, quelle que soit sa profondeur.

## 0. Message d'intro (obligatoire, avant toute question)

Avant de commencer, annonce brièvement à l'utilisateur (2-3 phrases) :
combien de phases suivent (entretien, recherche marché, diagnostic, relecture),
que l'entretien n'a pas de nombre de questions fixe, et que le rapport final
atterrira dans `outputs/report-YYYY-MM-DD.md`.

## 1. Interviewer — exécuté directement ici, pas via Task

Lis `memory/user-profile.md`. Mène l'entretien socratique en suivant
strictement `agents/interviewer.md` (4 phases, adaptatif, `AskUserQuestion`
uniquement, jamais de réponse supposée). Si un profil existant couvre déjà
certains points, confirme-les brièvement au lieu de tout redemander.

Mets à jour `memory/user-profile.md` et ajoute une ligne à
`memory/diagnostic-history.md` (colonne "Rapport généré" = `(en attente)`
pour l'instant). Retiens le résumé condensé du profil (objectif, stack,
niveau, langue préférée, marché cible recherche, contrainte principale,
tension clé) — c'est ce que tu transmets aux agents suivants. À partir de ce
moment, ta propre communication avec l'utilisateur (annonces, verdicts,
résumé final) suit la langue préférée du profil — français par défaut si le
champ est vide.

## 2. Researcher — vrai subagent Task

Avant de lancer une recherche, vérifie la fraîcheur : lis
`knowledge/market-trends.md` et `knowledge/job-postings-analysis.md`. Si une
entrée récente (< 2-4 semaines) correspond déjà au même objectif ET à la même
stack que le profil actuel, tu peux sauter cette étape et le signaler à
l'utilisateur. Sinon (objectif/stack différents, ou pas de donnée récente),
invoque le subagent `researcher` avec le profil condensé en entrée — y
compris le champ **Marché cible recherche**, que le Researcher utilise pour
piloter `--location`/`--country-indeed` du skill offres d'emploi.

## 3. Knowledge Builder — vrai subagent Task

Invoque le subagent `knowledge-builder` (aucun paramètre requis au-delà du
contexte du run — il lit `knowledge/raw/` lui-même). Attends sa sortie
structurée avant de continuer.

## 4. Strategist — vrai subagent Task

Invoque le subagent `strategist`. **Rappel important** : ce subagent ne peut
pas écrire de fichier lui-même (contrainte plateforme — `Write` est bloqué
pour les fichiers de type rapport livrable). Il te retourne **deux** contenus
complets en texte, chacun dans son propre bloc de code Markdown, précédés du
résumé structuré :
1. Le rapport tracé → tu l'écris tel quel dans `outputs/report-YYYY-MM-DD.md`
2. L'analyse basée sur son propre jugement → tu l'écris tel quel dans
   `outputs/analyse-modele-YYYY-MM-DD.md`

(Date du jour pour les deux ; écrase les fichiers du jour s'ils existent déjà,
ne touche jamais aux fichiers des jours précédents.)

## 5. Critic — vrai subagent Task

Invoque le subagent `critic` sur `outputs/report-YYYY-MM-DD.md` uniquement
(indique-lui le chemin exact, et précise "premier passage"). Le Critic ne
relit **pas** `outputs/analyse-modele-YYYY-MM-DD.md` — pas de critère de
traçabilité applicable à ce document, donc pas de relecture qualité dessus.

- Si le verdict est `APPROUVÉ` → passe à l'étape 6.
- Si le verdict est `CORRECTIONS REQUISES` → relance le subagent `strategist`
  une seule fois avec la liste des corrections exactes du Critic en entrée,
  ré-écris `outputs/report-YYYY-MM-DD.md` avec le nouveau contenu (l'analyse
  modèle déjà écrite à l'étape 4 n'a pas besoin d'être régénérée — les
  corrections du Critic ne portent que sur le rapport tracé), puis relance le
  subagent `critic` en précisant cette fois "second passage, rends un verdict
  final". N'itère pas au-delà de ce second passage, quel que soit le verdict
  (contrat : 1 cycle de correction maximum).

## 6. Sortie finale à l'utilisateur

Affiche, dans l'ordre :
- Les chemins des deux documents : `outputs/report-YYYY-MM-DD.md` et
  `outputs/analyse-modele-YYYY-MM-DD.md`
- Le verdict final du Critic sur le rapport (approuvé, ou corrigé une fois
  puis verdict final)
- Un résumé en 3-5 lignes du diagnostic (pas le contenu entier — l'utilisateur
  peut ouvrir les fichiers)
- Si le Critic a signalé un point d'attention hors des 3 critères (ex:
  couverture `knowledge/` insuffisante) : le mentionner explicitement, avec
  la recommandation associée (ex: relancer un `/diagnostic` plus tard une
  fois le marché mieux couvert)

Mets aussi à jour la colonne "Rapport généré" de la ligne correspondante dans
`memory/diagnostic-history.md` avec le chemin réel du rapport (remplace le
`(en attente)` posé à l'étape 1).
