# Analyse des offres d'emploi

<!-- FORMAT OBLIGATOIRE par batch (champs manquants = batch invalide) :
- Objectif visé : [CDI | Freelance | Remote international | ...]
- Stack cible : [liste des technos filtrées]
- Date d'analyse : YYYY-MM-DD
- Nombre d'offres analysées : N
- Sources : [plateformes scrapées via python-jobspy]
-->

<!-- Exemple d'entrée correcte :

## Batch YYYY-MM-DD — CDI Backend Python / Paris + Remote

**Offres analysées :** 47
**Sources :** Indeed, LinkedIn (via python-jobspy)
**Objectif visé :** CDI Backend
**Stack cible :** Python, Django/FastAPI

### Compétences les plus demandées
- Python (100% des offres)
- Docker (78%)
- PostgreSQL (65%)
- ...

### Fourchettes salariales observées
- Junior (0-2 ans) : 38-45k€
- Confirmé (3-5 ans) : 48-60k€
- Senior (6+ ans) : 62-80k€

### Patterns notables
- 60% des offres mentionnent Kubernetes comme "nice to have"
- Remote full accepté dans 35% des offres analysées
- ...

-->

## Batch 2026-08-06 — Lead Technique / Staff Engineer / Paris (recherche "Lead Technique Backend")

**Offres analysées :** 100
**Sources :** Indeed, LinkedIn (via python-jobspy)
**Objectif visé :** Lead Technique / Staff Engineer
**Stack cible :** Python, Django, FastAPI, PostgreSQL, AWS, Docker

### Compétences les plus demandées
(fréquence des termes de la stack cible détectés dans description/skills des offres)
- Python (16%)
- AWS (14%)
- PostgreSQL (13%)
- Docker (12%)
- FastAPI (6%)
- Django (3%)

### Fourchettes salariales observées
Aucune donnée salariale exploitable dans ce batch (aucune des 100 offres ne
renseigne `min_amount`/`max_amount`).

### Patterns notables
- Seulement 8% des offres marquées `is_remote: true` — le remote reste
  minoritaire sur cette recherche côté Paris.
- `job_type` renseigné sur 13% des offres seulement (toutes en "fulltime"
  quand présent) ; 87% sans valeur exploitable.
- `company_industry` renseigné sur seulement 8 offres/100 — trop parcellaire
  pour dégager un secteur dominant fiable. Sur les valeurs présentes :
  Consulting And Business Services (3), Internet And Software (2), Human
  Resources And Staffing (2), Health Care (1).
- Répartition égale des sources : 50 offres Indeed / 50 offres LinkedIn.
- Titres les plus fréquents dans l'échantillon : "Lead développeur back-end
  et intéropérabilité H/F" (4 occurrences), "Tech Lead - Full Stack - Défense
  & Sécurité - Ile de France" (2), "Tech lead" (2) — cohérent avec la
  recherche "Lead Technique Backend".

## Batch 2026-08-06 — Lead Technique / Staff Engineer / Paris (recherche "Staff Engineer")

**Offres analysées :** 100
**Sources :** Indeed, LinkedIn (via python-jobspy)
**Objectif visé :** Lead Technique / Staff Engineer
**Stack cible :** Python, Django, FastAPI, PostgreSQL, AWS, Docker

### Compétences les plus demandées
(fréquence des termes de la stack cible détectés dans description/skills des offres)
- Python (22%)
- AWS (16%)
- Docker (7%)
- PostgreSQL (6%)
- Django (2%)
- FastAPI (1%)

### Fourchettes salariales observées
Aucune donnée salariale exploitable dans ce batch (aucune des 100 offres ne
renseigne `min_amount`/`max_amount`).

### Patterns notables
- 23% des offres marquées `is_remote: true` — remote plus fréquent que sur la
  recherche "Lead Technique Backend" (8%), cohérent avec un rôle IC senior
  (Staff Engineer) plus souvent ouvert au remote que les rôles Lead
  Technique/managériaux.
- `job_type` renseigné sur 26% des offres seulement (toutes en "fulltime"
  quand présent) ; 74% sans valeur exploitable.
- `company_industry` renseigné sur 30 offres/100. Dominante : Internet And
  Software (8), suivie de Retail (4), Computers And Electronics (3) —
  cohérent avec un rôle Staff Engineer typiquement concentré dans le secteur
  tech/logiciel.
- Répartition égale des sources : 50 offres Indeed / 50 offres LinkedIn.
- Titres les plus fréquents dans l'échantillon : plusieurs déclinaisons de
  "Staff Engineer" / "Staff Software Engineer" / "Staff Backend Engineer
  (Ruby)" et "Senior Software Engineer" — échantillon cohérent avec la
  recherche "Staff Engineer", avec des postes touchant des domaines variés
  (ASIC/SoC chez Qualcomm, AI Developer Experience, Platform & Reliability).
