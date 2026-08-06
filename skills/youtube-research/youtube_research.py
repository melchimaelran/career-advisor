#!/usr/bin/env python3
"""
YouTube research skill — career-advisor.
Searches YouTube by keyword or URL, extracts transcripts, writes Markdown to output-dir.
Called by the Researcher agent via Bash. No API key required.

Usage:
  python youtube_research.py --query "backend Python marché 2025" --max-results 5
  python youtube_research.py --url "https://youtube.com/watch?v=VIDEO_ID"
"""

import argparse
import glob
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

TRANSCRIPT_MAX_CHARS = 60_000


def parse_args():
    parser = argparse.ArgumentParser(description="YouTube research skill")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--query", help="Keyword search query")
    group.add_argument("--url", help="Direct YouTube video or playlist URL")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--output-dir", default="knowledge/raw")
    parser.add_argument("--sources-log", default="knowledge/sources-log.md")
    return parser.parse_args()


def format_duration(seconds):
    if not seconds:
        return "??:??"
    seconds = int(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_upload_date(upload_date):
    # yt-dlp returns YYYYMMDD
    if not upload_date or len(str(upload_date)) != 8:
        return upload_date or "inconnue"
    s = str(upload_date)
    return f"{s[:4]}-{s[4:6]}-{s[6:]}"


def _ytdlp_bin():
    # Use yt-dlp from the same venv as this Python, falling back to PATH
    candidate = os.path.join(os.path.dirname(sys.executable), "yt-dlp")
    return candidate if os.path.isfile(candidate) else "yt-dlp"


def run_ytdlp(args):
    result = subprocess.run(
        [_ytdlp_bin()] + args + ["--no-warnings"],
        capture_output=True,
        text=True,
    )
    videos = []
    for line in result.stdout.strip().splitlines():
        line = line.strip()
        if line:
            try:
                videos.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return videos


def get_videos_from_query(query, max_results):
    print(f"[youtube-research] Recherche: {query!r} (max {max_results})")
    return run_ytdlp([f"ytsearch{max_results}:{query}", "--flat-playlist", "-j"])


def get_videos_from_url(url):
    print(f"[youtube-research] Résolution URL: {url}")
    return run_ytdlp([url, "--flat-playlist", "-j"])


def check_cache(output_dir, video_id, max_age_days=28):
    pattern = os.path.join(output_dir, f"youtube-*-{video_id}.md")
    matches = glob.glob(pattern)
    if not matches:
        return None
    newest = max(matches, key=os.path.getmtime)
    age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(newest))
    return newest if age < timedelta(days=max_age_days) else None


def fetch_transcript(video_id):
    api = YouTubeTranscriptApi()
    try:
        try:
            result = api.fetch(video_id, languages=["fr", "en"])
        except NoTranscriptFound:
            # Fall back to any available language
            transcript_list = api.list(video_id)
            result = next(iter(transcript_list)).fetch()

        text = " ".join(s.text for s in result)
        if len(text) > TRANSCRIPT_MAX_CHARS:
            text = text[:TRANSCRIPT_MAX_CHARS] + "\n\n[transcript tronqué à 60 000 chars]"
        return text
    except (TranscriptsDisabled, NoTranscriptFound, StopIteration):
        return None


def write_markdown(output_dir, video_id, title, channel, upload_date, duration, transcript):
    today = datetime.now().strftime("%Y-%m-%d")
    filepath = os.path.join(output_dir, f"youtube-{today}-{video_id}.md")

    lines = [
        f"# {title}",
        "",
        f"**URL :** https://youtube.com/watch?v={video_id}",
        f"**Chaîne :** {channel or 'inconnue'}",
        f"**Date de publication :** {format_upload_date(upload_date)}",
        f"**Date de récupération :** {today}",
        f"**Durée :** {format_duration(duration)}",
        "",
        "## Transcript",
        "",
        transcript if transcript else "_Transcript non disponible._",
    ]

    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    return filepath


def append_log(log_path, date, video_id, status, detail):
    detail = detail.replace("|", "/").replace("\n", " ")[:100]
    entry = f"| {date} | YouTube/{video_id} | {status} | {detail} |\n"

    log_dir = os.path.dirname(log_path)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    if not os.path.exists(log_path):
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("# sources-log\n\n| Date | Source | Statut | Détail |\n|------|--------|--------|--------|\n")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


def main():
    args = parse_args()
    today = datetime.now().strftime("%Y-%m-%d")

    if args.query:
        videos = get_videos_from_query(args.query, args.max_results)
    else:
        videos = get_videos_from_url(args.url)

    if not videos:
        print("[youtube-research] ERREUR: aucune vidéo trouvée", file=sys.stderr)
        append_log(args.sources_log, today, "N/A", "ERREUR", "Aucune vidéo trouvée")
        return

    print(f"[youtube-research] {len(videos)} vidéo(s) à traiter")
    ok, cached, errors = 0, 0, 0

    for video in videos:
        video_id = video.get("id") or ""
        title = video.get("title") or video.get("webpage_url_basename") or video_id
        channel = video.get("channel") or video.get("uploader") or ""
        upload_date = video.get("upload_date") or ""
        duration = video.get("duration")

        if not video_id:
            print(f"[youtube-research] Skip: ID manquant pour {title!r}", file=sys.stderr)
            errors += 1
            continue

        # Cache
        cached_path = check_cache(args.output_dir, video_id)
        if cached_path:
            print(f"[youtube-research] CACHE: {title!r}")
            append_log(args.sources_log, today, video_id, "CACHE", title)
            cached += 1
            continue

        # Fetch + write
        print(f"[youtube-research] Fetch: {title!r} ({video_id})")
        try:
            transcript = fetch_transcript(video_id)
            write_markdown(args.output_dir, video_id, title, channel, upload_date, duration, transcript)
            append_log(args.sources_log, today, video_id, "OK", title)
            ok += 1
        except Exception as e:
            msg = str(e)
            print(f"[youtube-research] ERREUR {video_id}: {msg}", file=sys.stderr)
            append_log(args.sources_log, today, video_id, "ERREUR", msg)
            errors += 1

    print(f"[youtube-research] Terminé — OK: {ok}, cache: {cached}, erreurs: {errors}")


if __name__ == "__main__":
    main()
