# Skill : job-postings-research

Basé sur [python-jobspy](https://github.com/Bunsly/JobSpy).
Gratuit, pas de connexion à un compte personnel requise.

## Objectif

Scraper des offres d'emploi sur les plateformes principales pour alimenter le
Researcher en données réelles de marché (compétences demandées, salaires, patterns).

## ⚠️ Avertissement

Scraping non officiel — peut casser si les plateformes changent leur structure.
La règle de repli est obligatoire (voir section dédiée).

## Installation

```bash
cd skills/job-postings-research
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Pas de clé API. Pas de compte connecté. Exécution 100% locale.

## Invocation

```bash
# Depuis la racine du projet
.venv/bin/python skills/job-postings-research/job_postings_research.py \
  --search-term "développeur backend Python" \
  --location "Paris" \
  --results-wanted 50 \
  --site-names indeed,linkedin \
  --objective "CDI Backend" \
  --stack "Python,Django,FastAPI,Docker"
```

## Inputs

| Paramètre | Type | Description |
|-----------|------|-------------|
| `--search-term` | string | Intitulé du poste (ex: "développeur backend Python") — requis |
| `--location` | string | Localisation (ex: "Paris" ou "Remote") |
| `--results-wanted` | int | Nombre d'offres cibles (défaut : 50) |
| `--site-names` | liste (virgules) | Plateformes (défaut : `indeed,linkedin`) |
| `--country-indeed` | string | Pays pour le scraping Indeed (défaut : `france` — Indeed géolocalise par domaine pays, sans ça une recherche "Paris" tape le domaine US et ne renvoie rien) |
| `--objective` | string | Label "Objectif visé" du batch (ex: "CDI Backend") |
| `--stack` | liste (virgules) | Mots-clés stack (ex: "Python,Django,Docker") — sert à la fois de label "Stack cible" et de base pour compter les compétences les plus demandées |
| `--cache-max-age-days` | int | Âge max du cache avant re-scraping (défaut : 28, cohérent avec la règle de fraîcheur de `CLAUDE.md`) |

## Outputs

Fichier JSON brut dans `knowledge/raw/` + batch ajouté à
`knowledge/job-postings-analysis.md` :

```
knowledge/raw/jobs-YYYY-MM-DD-[slug-recherche].json   ← données brutes (offres dédupliquées)
```

Le batch Markdown suit le format déjà documenté dans
`knowledge/job-postings-analysis.md` (objectif, stack, date, sources,
compétences les plus demandées, fourchettes salariales, patterns notables).

## Fonctionnement

1. **Vérification cache** : si `knowledge/raw/jobs-*-[slug].json` existe et
   date de moins de `--cache-max-age-days` → skip le scraping, log `CACHE`
2. **Scraping site par site** (pas un seul appel multi-sites) : chaque
   plateforme de `--site-names` est scrapée dans sa propre requête
   `scrape_jobs(site_name=[site], ...)`, avec `try/except` individuel — une
   plateforme qui échoue ne bloque pas les autres :
   ```python
   from jobspy import scrape_jobs

   for site in site_names:
       try:
           df = scrape_jobs(site_name=[site], search_term=..., location=...,
                             results_wanted=..., country_indeed="france")
       except Exception as e:
           # log l'échec, continue avec le site suivant
           ...
   ```
3. **Dédoublonnage** : concat des résultats + `drop_duplicates(subset=["job_url"])`
4. **Analyse** : comptage des mots-clés `--stack` dans titre+description,
   stats salariales min/max/médiane (si disponibles), % remote — pas de
   ventilation par séniorité (donnée non fournie par les sources scrapées,
   explicitement notée comme limite dans le batch)

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
