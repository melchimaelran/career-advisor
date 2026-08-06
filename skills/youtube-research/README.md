# Skill : youtube-research

Adapté de [zerowing113/claude-youtube-skill](https://github.com/zerowing113/claude-youtube-skill).
Gratuit, local, pas de clé API requise.

## Objectif

Rechercher des vidéos YouTube par mot-clé et en extraire les transcripts pour
alimenter le Researcher en contenu vidéo francophone/anglophone sur le marché tech.

## Installation

```bash
cd skills/youtube-research
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Pas de clé API. Pas de compte YouTube. Exécution 100% locale.

## Invocation

```bash
# Depuis la racine du projet
.venv/bin/python skills/youtube-research/youtube_research.py --query "..." --max-results 5
# ou depuis skills/youtube-research/
.venv/bin/python youtube_research.py --query "..."
```

## Inputs

| Paramètre | Type | Description |
|-----------|------|-------------|
| `query` | string | Mot-clé de recherche (ex: "développeur backend marché 2024") |
| `max_results` | int | Nombre max de vidéos à traiter (défaut : 5) |
| `url` | string | URL directe d'une vidéo ou playlist (optionnel, alternative à `query`) |

## Outputs

Pour chaque vidéo traitée, un fichier Markdown dans `knowledge/raw/` :

```
knowledge/raw/youtube-YYYY-MM-DD-[slug-titre].md
```

Format du fichier :
```markdown
# [Titre de la vidéo]

**URL :** https://youtube.com/watch?v=...
**Chaîne :** [nom de la chaîne]
**Date de publication :** YYYY-MM-DD
**Date de récupération :** YYYY-MM-DD
**Durée :** MM:SS

## Transcript

[transcript complet ou résumé si trop long]
```

## Fonctionnement

1. **Recherche par mot-clé** : `yt-dlp "ytsearch{max_results}:{query}" --flat-playlist`
2. **Vérification cache** : si `knowledge/raw/youtube-*-[video-id].md` existe et
   date de moins de 4 semaines → skip (ne pas re-fetcher)
3. **Fetch transcript** : `youtube-transcript-api` avec priorité de langue :
   français → anglais → auto-généré
4. **Fallback metadata** : si pas de transcript disponible → sauvegarder uniquement
   le titre, la description et l'URL

## Comportement de repli

Si le skill échoue (quota YouTube, vidéo privée, pas de transcript) :
- Continuer avec les vidéos suivantes
- Logger l'échec dans `knowledge/sources-log.md`
- Ne jamais bloquer le run du Researcher

## Modifications vs repo d'origine

- Ajout recherche par mot-clé (`yt-dlp ytsearchN:`)
- Priorité langue française dans les transcripts
- Ajout vérification de cache avant fetch
- Suppression de la logique de compilation Obsidian (inutile ici)
