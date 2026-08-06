# Skill : action-plan-builder

Templates des deux documents produits par le Strategist :
`outputs/report-YYYY-MM-DD.md` (rapport tracé, relu par le Critic) et
`outputs/analyse-modele-YYYY-MM-DD.md` (second avis basé sur le jugement du
modèle, non relu par le Critic — pas soumis à la règle de traçabilité).

## Objectif

Définir la structure obligatoire du rapport `outputs/report-YYYY-MM-DD.md`.
Toute section manquante ou action sans critère de "fait" = rapport incomplet.

Structure ci-dessous en français = référence par défaut. Si `Langue préférée`
du profil ≠ français, le Strategist traduit les titres de section dans cette
langue en gardant structure et ordre identiques.

## Structure obligatoire du rapport

```markdown
# Rapport de diagnostic carrière — YYYY-MM-DD

**Profil :** [Métier] — [Niveau] — [Stack principale]
**Objectif visé :** [type de poste]
**Généré le :** YYYY-MM-DD

---

## 1. Résumé du diagnostic

[1 page max — profil actuel vs profil cible marché]
[Les écarts principaux en 3-5 points]

---

## 2. Analyse

### Forces
[Ce que l'utilisateur a déjà, valorisé par le marché pour l'objectif visé]
- ...

### Faiblesses
[Écarts entre profil actuel et attentes du marché]
- ...

### Compétences manquantes
[Absentes du profil mais attendues/requises pour l'objectif visé]
- ...

### Avantages compétitifs
[Ce qui différencie positivement l'utilisateur vs d'autres candidats]
- ...

### Blocages
[Obstacles concrets identifiés en phase 4 de l'Interviewer]
- ...

### Opportunités
[Niches, tendances marché favorables au profil — sourcées dans knowledge/]
- ...

---

## 3. Plan d'action — 30 jours

> Objectif : [ce que l'utilisateur peut réaliser en 30 jours]

| Action | Critère de "fait" | Priorité |
|--------|-------------------|----------|
| [Action concrète] | [Comment savoir que c'est fait ?] | P0/P1/P2 |

---

## 4. Plan d'action — 90 jours

> Objectif : [ce que l'utilisateur peut réaliser en 90 jours]

| Action | Critère de "fait" | Priorité |
|--------|-------------------|----------|
| ... | ... | ... |

---

## 5. Plan d'action — 365 jours

> Objectif : [ce que l'utilisateur peut réaliser en 1 an]

| Action | Critère de "fait" | Priorité |
|--------|-------------------|----------|
| ... | ... | ... |

---

## Sources

[Liste de toutes les sources citées dans ce rapport]
- [Titre](URL) — `knowledge/market-trends.md`, récupéré le YYYY-MM-DD
- ...
```

## Règles du Critic (critères de validation)

Ces critères s'appliquent uniquement à `outputs/report-YYYY-MM-DD.md` — le
Critic ne relit pas `outputs/analyse-modele-YYYY-MM-DD.md` (voir plus bas).

1. **Concrétude** : chaque action a un critère de "fait" vérifiable
   - KO : "Améliorer ses compétences en React"
   - OK : "Terminer le projet X avec React, le déployer sur Vercel"

2. **Personnalisation** : les plans respectent les contraintes réelles (temps,
   risque, localisation) identifiées en phase 4 de l'Interviewer

3. **Traçabilité** : toute affirmation factuelle pointe vers une source dans
   `knowledge/` — pas d'assertion sans origine

## Structure obligatoire de `outputs/analyse-modele-YYYY-MM-DD.md`

Plus léger que le rapport principal — pas de contrainte de traçabilité, mais
toujours de la concrétude et de la personnalisation (voir
`agents/strategist.md`, section "Second document").

```markdown
# Analyse — perspective du modèle — YYYY-MM-DD

> **Avertissement :** ce document reflète le jugement général du modèle
> (connaissances d'entraînement), pas une recherche marché vérifiée ni
> sourcée dans `knowledge/`. À lire comme un second avis complémentaire —
> pas un substitut à `outputs/report-YYYY-MM-DD.md`, qui reste la référence
> tracée.

**Profil :** [Métier] — [Niveau] — [Stack principale]
**Objectif visé :** [type de poste]
**Généré le :** YYYY-MM-DD

---

## Lecture du marché par le modèle

[Ce que le modèle sait du segment visé — tendances générales, demande,
rémunération indicative — en précisant le niveau de confiance/actualité]

## Cohérence perçue de la stratégie

[Regard neuf sur la stratégie déclarée par l'utilisateur, au-delà des
tensions déjà identifiées par l'Interviewer]

## Angles morts / risques non couverts par knowledge/

- ...

## Recommandations complémentaires

| Recommandation | Critère de "fait" | Priorité |
|-----------------|-------------------|----------|
| [Action concrète] | [Comment savoir que c'est fait ?] | P0/P1/P2 |
```
