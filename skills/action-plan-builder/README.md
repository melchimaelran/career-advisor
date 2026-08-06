# Skill : action-plan-builder

Template du rapport final produit par le Strategist et relu par le Critic.

## Objectif

Définir la structure obligatoire du rapport `outputs/report-YYYY-MM-DD.md`.
Toute section manquante ou action sans critère de "fait" = rapport incomplet.

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

1. **Concrétude** : chaque action a un critère de "fait" vérifiable
   - KO : "Améliorer ses compétences en React"
   - OK : "Terminer le projet X avec React, le déployer sur Vercel"

2. **Personnalisation** : les plans respectent les contraintes réelles (temps,
   risque, localisation) identifiées en phase 4 de l'Interviewer

3. **Traçabilité** : toute affirmation factuelle pointe vers une source dans
   `knowledge/` — pas d'assertion sans origine
