#!/usr/bin/env python3
"""
Job postings research skill — career-advisor.
Scrapes job postings via python-jobspy, writes raw JSON + a Markdown analysis
batch. Called by the Researcher agent via Bash. No API key, no login required.

Usage:
  python job_postings_research.py --search-term "développeur backend Python" \
    --location "Paris" --results-wanted 50 --site-names indeed,linkedin \
    --objective "CDI Backend" --stack "Python,Django,FastAPI,Docker"
"""

import argparse
import glob
import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timedelta

import pandas as pd
from jobspy import scrape_jobs


def parse_args():
    parser = argparse.ArgumentParser(description="Job postings research skill")
    parser.add_argument("--search-term", required=True)
    parser.add_argument("--location", default="")
    parser.add_argument("--results-wanted", type=int, default=50)
    parser.add_argument("--site-names", default="indeed,linkedin")
    parser.add_argument("--country-indeed", default="france")
    parser.add_argument("--objective", default="")
    parser.add_argument("--stack", default="")
    parser.add_argument("--output-dir", default="knowledge/raw")
    parser.add_argument("--sources-log", default="knowledge/sources-log.md")
    parser.add_argument("--analysis-file", default="knowledge/job-postings-analysis.md")
    parser.add_argument("--cache-max-age-days", type=int, default=28)
    return parser.parse_args()


def slugify(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "requete"


def check_cache(output_dir, slug, max_age_days):
    pattern = os.path.join(output_dir, f"jobs-*-{slug}.json")
    matches = glob.glob(pattern)
    if not matches:
        return None
    newest = max(matches, key=os.path.getmtime)
    age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(newest))
    return newest if age < timedelta(days=max_age_days) else None


def append_log(log_path, date, source, status, detail):
    detail = detail.replace("|", "/").replace("\n", " ")[:100]
    entry = f"| {date} | {source} | {status} | {detail} |\n"

    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("# sources-log\n\n| Date | Source | Statut | Détail |\n|------|--------|--------|--------|\n")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def scrape_all_sites(site_names, search_term, location, results_wanted, country_indeed):
    """Scrape site-by-site so one failing platform never blocks the others."""
    frames = []
    site_results = {}  # site -> (count, error|None)

    for site in site_names:
        try:
            df = scrape_jobs(
                site_name=[site],
                search_term=search_term,
                location=location or None,
                results_wanted=results_wanted,
                country_indeed=country_indeed,
            )
            count = 0 if df is None else len(df)
            site_results[site] = (count, None)
            if count:
                frames.append(df)
        except Exception as e:
            site_results[site] = (0, str(e))
            continue

    if frames:
        combined = pd.concat(frames, ignore_index=True)
        if "job_url" in combined.columns:
            combined = combined.drop_duplicates(subset=["job_url"])
    else:
        combined = pd.DataFrame()

    return combined, site_results


def compute_skill_counts(df, stack):
    total = len(df)
    if not stack or total == 0:
        return None

    text_cols = [c for c in ("title", "description") if c in df.columns]
    if not text_cols:
        return None

    combined_text = df[text_cols].fillna("").agg(" ".join, axis=1).str.lower()

    counts = []
    for keyword in stack:
        kw = keyword.strip()
        if not kw:
            continue
        hits = combined_text.str.contains(re.escape(kw.lower())).sum()
        counts.append((kw, hits, round(100 * hits / total)))

    counts.sort(key=lambda x: x[1], reverse=True)
    return counts


def compute_salary_stats(df):
    if "min_amount" not in df.columns or "max_amount" not in df.columns:
        return None

    salaried = df.dropna(subset=["min_amount", "max_amount"], how="all")
    if salaried.empty:
        return None

    mins = salaried["min_amount"].dropna()
    maxs = salaried["max_amount"].dropna()
    if mins.empty and maxs.empty:
        return None

    return {
        "count": len(salaried),
        "min": mins.min() if not mins.empty else None,
        "max": maxs.max() if not maxs.empty else None,
        "median_min": mins.median() if not mins.empty else None,
        "median_max": maxs.median() if not maxs.empty else None,
    }


def compute_remote_pct(df):
    if "is_remote" not in df.columns or len(df) == 0:
        return None
    return round(100 * df["is_remote"].fillna(False).astype(bool).sum() / len(df))


def write_json(output_dir, slug, today, search_term, location, objective, stack, sources, df):
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"jobs-{today}-{slug}.json")

    payload = {
        "date": today,
        "search_term": search_term,
        "location": location,
        "objective": objective,
        "stack": stack,
        "sources": sources,
        "count": len(df),
        "jobs": json.loads(df.to_json(orient="records")) if not df.empty else [],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return filepath


def append_analysis_batch(analysis_file, today, search_term, objective, stack,
                           sources_ok, df, skill_counts, salary_stats, remote_pct):
    objective_label = objective or "(non précisé)"
    stack_label = ", ".join(stack) if stack else "(non précisée)"

    lines = [
        "",
        f"## Batch {today} — {objective_label} / {search_term}",
        "",
        f"**Offres analysées :** {len(df)}",
        f"**Sources :** {', '.join(sources_ok) if sources_ok else 'aucune (voir sources-log.md)'}",
        f"**Objectif visé :** {objective_label}",
        f"**Stack cible :** {stack_label}",
        "",
    ]

    if skill_counts:
        lines.append("### Compétences les plus demandées")
        for kw, hits, pct in skill_counts:
            lines.append(f"- {kw} ({pct}% des offres)")
        lines.append("")
    else:
        lines.append("### Compétences les plus demandées")
        lines.append("_Non calculé — aucun `--stack` fourni ou aucune offre récupérée._")
        lines.append("")

    lines.append("### Fourchettes salariales observées")
    if salary_stats:
        lines.append(
            f"- {salary_stats['count']} offre(s) avec données salariales : "
            f"{salary_stats['min']:.0f}–{salary_stats['max']:.0f} "
            f"(médiane {salary_stats['median_min']:.0f}–{salary_stats['median_max']:.0f})"
        )
    else:
        lines.append("_Aucune donnée salariale exploitable dans ce batch._")
    lines.append("")

    lines.append("### Patterns notables")
    if remote_pct is not None:
        lines.append(f"- {remote_pct}% des offres marquées remote")
    lines.append(
        "- Pas de ventilation par séniorité (junior/confirmé/senior) : donnée "
        "non disponible depuis les sources scrapées"
    )
    lines.append("")

    if not os.path.exists(analysis_file):
        os.makedirs(os.path.dirname(analysis_file) or ".", exist_ok=True)
        with open(analysis_file, "w", encoding="utf-8") as f:
            f.write("# Analyse des offres d'emploi\n")

    with open(analysis_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    args = parse_args()
    today = datetime.now().strftime("%Y-%m-%d")
    site_names = [s.strip() for s in args.site_names.split(",") if s.strip()]
    stack = [s.strip() for s in args.stack.split(",") if s.strip()]
    slug = slugify(f"{args.search_term}-{args.location}")

    cached_path = check_cache(args.output_dir, slug, args.cache_max_age_days)
    if cached_path:
        print(f"[job-postings-research] CACHE: {cached_path!r} ({args.cache_max_age_days}j)")
        append_log(args.sources_log, today, f"jobs/{slug}", "CACHE", cached_path)
        return

    print(f"[job-postings-research] Recherche: {args.search_term!r} @ {args.location!r} "
          f"sur {site_names} (max {args.results_wanted})")

    df, site_results = scrape_all_sites(site_names, args.search_term, args.location,
                                         args.results_wanted, args.country_indeed)

    sources_ok = []
    for site, (count, error) in site_results.items():
        if error is None:
            sources_ok.append(site)
            append_log(args.sources_log, today, f"jobs/{site}", "OK", f"{count} offre(s) — {args.search_term}")
            print(f"[job-postings-research] OK {site}: {count} offre(s)")
        else:
            append_log(args.sources_log, today, f"jobs/{site}", "ERREUR", error)
            print(f"[job-postings-research] ERREUR {site}: {error}", file=sys.stderr)

    if df.empty:
        print("[job-postings-research] ERREUR: aucune offre récupérée sur aucune plateforme", file=sys.stderr)
        append_log(args.sources_log, today, f"jobs/{slug}", "ERREUR", "Toutes les plateformes ont échoué")
        return

    json_path = write_json(args.output_dir, slug, today, args.search_term, args.location,
                            args.objective, stack, sources_ok, df)

    skill_counts = compute_skill_counts(df, stack)
    salary_stats = compute_salary_stats(df)
    remote_pct = compute_remote_pct(df)

    append_analysis_batch(args.analysis_file, today, args.search_term, args.objective, stack,
                           sources_ok, df, skill_counts, salary_stats, remote_pct)

    print(f"[job-postings-research] Terminé — {len(df)} offre(s) dédupliquées, "
          f"JSON: {json_path}, analyse ajoutée à {args.analysis_file}")


if __name__ == "__main__":
    main()
