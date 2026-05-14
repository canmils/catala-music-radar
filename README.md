# Catalan Music Radar

A Python tool to track Catalan music artists, playlists, and recent releases using public music data sources.

## Features

- Track a list of Catalan artists
- Read Spotify playlist inputs
- Collect MusicBrainz release data
- Export results to CSV
- Separate recent, upcoming, unknown-date, and failed records

## Requirements

- Python 3.10+
- Spotify developer credentials, only if using the Spotify collector

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Environment variables

Create a local `.env` file or set these variables in PowerShell:

```powershell
$env:SPOTIFY_CLIENT_ID="your-client-id"
$env:SPOTIFY_CLIENT_SECRET="your-client-secret"
```

## Run

```powershell
python .\src\main.py
```

## Output

Generated CSV reports are stored in:

```text
output/
```

## Status

Prototype / portfolio project focused on music discovery workflows and public data aggregation.
