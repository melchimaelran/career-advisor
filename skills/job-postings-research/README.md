# Skill : job-postings-research

Basé sur [python-jobspy](https://github.com/Bunsly/JobSpy).
Gratuit, pas de connexion à un compte personnel requise.

## Objectif

Scraper des offres d'emploi sur les plateformes principales pour alimenter le
Researcher en données réelles de marché (compétences demandées, salaires, patterns).

## ⚠️ Avertissement

Scraping non officiel — peut casser si les plateformes changent leur structure.
La règle de repli est obligatoire (voir section dédiée).

## Dépendances

```bash
pip install python-jobspy
```

## Inputs

| Paramètre | Type | Description |
|-----------|------|-------------|
| `search_term` | string | Intitulé du poste (ex: "développeur backend Python") |
| `location` | string | Localisation (ex: "Paris" ou "Remote") |
| `results_wanted` | int | Nombre d'offres cibles (défaut : 50) |
| `site_names` | list | Plateformes (défaut : `["indeed", "linkedin"]`) |

## Outputs

Fichier JSON + Markdown résumé dans `knowledge/raw/` :

```
knowledge/raw/jobs-YYYY-MM-DD-[slug-query].json     ← données brutes
knowledge/raw/jobs-YYYY-MM-DD-[slug-query].md       ← résumé structuré
```

Le fichier Markdown suit le format de `knowledge/job-postings-analysis.md`.

## Fonctionnement

```python
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=["indeed", "linkedin"],
    search_term="développeur backend Python",
    location="Paris",
    results_wanted=50,
)
```

## Règle de repli (obligatoire)

| Situation | Action |
|-----------|--------|
| Une plateforme renvoie une erreur | Continuer avec les autres plateformes |
| Toutes les plateformes échouent | Logger dans `sources-log.md`, signaler au Researcher |
| Moins d'offres que `results_wanted` | Continuer avec ce qui est disponible |

Logger systématiquement dans `knowledge/sources-log.md` :
- Plateformes tentées
- Nombre d'offres récupérées
- Erreurs éventuelles

**Ne jamais bloquer le run.**
