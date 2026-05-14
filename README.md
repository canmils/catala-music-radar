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