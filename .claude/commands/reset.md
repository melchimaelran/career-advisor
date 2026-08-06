---
description: Efface le profil utilisateur et la connaissance marché pour repartir de zéro (garde les rapports passés dans outputs/)
---

Cette commande est **destructive et irréversible** pour `memory/` et
`knowledge/raw/` (gitignorés — aucun historique git pour les récupérer).
Ne l'exécute jamais sans confirmation explicite.

## 1. Confirmation obligatoire avant toute action

Utilise `AskUserQuestion` pour demander confirmation, en listant précisément
ce qui va être effacé :

- `memory/user-profile.md` → remis au template vide
- `memory/diagnostic-history.md` → remis au template vide
- `knowledge/market-trends.md` → remis au template vide
- `knowledge/job-postings-analysis.md` → remis au template vide
- `knowledge/sources-log.md` → remis au template vide
- `knowledge/raw/*` → supprimés (sauf `.gitkeep`)

Précise explicitement ce qui **n'est pas touché** : `outputs/` (rapports
passés conservés comme archive).

Si l'utilisateur n'confirme pas → arrête-toi là, ne modifie rien, dis-le
clairement.

## 2. Si confirmé — remise à blanc

Remets chaque fichier à son contenu template d'origine (pas de suppression de
fichier hors `knowledge/raw/` — la structure et les blocs de commentaire de
format doivent rester identiques à l'état "Fondations" du projet) :

**`memory/user-profile.md`** :
```markdown
# Profil utilisateur

*Mis à jour le : [date du dernier run de l'Interviewer — à remplir par l'agent]*

---

## Situation actuelle

- **Métier :** ...
- **Niveau :** [Junior | Confirmé | Senior]
- **Années d'expérience :** ...
- **Stack principale :** ...
- **Type de contrat actuel :** [CDI | Freelance | Sans emploi | Alternance | ...]
- **Secteur :** ...
- **Localisation :** ...

## Objectifs déclarés

- **Type de poste visé :** [CDI | Freelance | Remote international | Produit | Consulting]
- **Horizon temporel :** ...
- **Critères prioritaires :** [salaire | autonomie | impact | stabilité | ...]
- **Détail des objectifs :** ...

## Tensions identifiées (phase socratique)

*(Écarts entre objectifs déclarés et réalité — rempli par l'Interviewer)*

- ...

## Contraintes réelles

- **Temps disponible pour se former (h/semaine) :** ...
- **Tolérance au risque financier :** [Faible | Moyenne | Élevée]
- **Mobilité géographique :** [Aucune | Région | France | International]
- **Contraintes personnelles :** ...

## Compétences actuelles

### Maîtrisées

- ...

### En cours d'apprentissage

- ...

### Identifiées comme manquantes (auto-évaluation)

- ...
```

**`memory/diagnostic-history.md`** :
```markdown
# Historique des diagnostics

Un run = une ligne. Permet de suivre l'évolution dans le temps et de retrouver
les rapports passés.

| Date | Objectif visé | Stack | Rapport généré |
|------|--------------|-------|----------------|
| — | — | — | Aucun run effectué |
```

**`knowledge/market-trends.md`** — garde uniquement les deux blocs de
commentaire HTML (format obligatoire + exemple), supprime toutes les entrées
ajoutées depuis.

**`knowledge/job-postings-analysis.md`** — garde uniquement les deux blocs de
commentaire HTML (format obligatoire + exemple), supprime tous les batches
ajoutés depuis.

**`knowledge/sources-log.md`** :
```markdown
# Log des sources

Utilisé par le Researcher pour logger les succès et les échecs de chaque source.
La règle de repli s'applique : un échec ne bloque pas le run — on continue et on
log ici.

| Date | Source | Statut | Détail |
|------|--------|--------|--------|
| — | — | — | Aucun run effectué |
```

**`knowledge/raw/`** : supprime tous les fichiers sauf `.gitkeep`.

## 3. Confirmation finale

Affiche à l'utilisateur la liste de ce qui a été effacé/remis à blanc, et
rappelle que `outputs/` n'a pas été touché — un `/diagnostic` peut être lancé
immédiatement pour repartir sur un profil neuf.
