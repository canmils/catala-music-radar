# Catalan Music Radar

A local CSV collector for releases by an artist list you curate, using MusicBrainz and optionally Spotify playlists. It helps organize discovery research. Inclusion in your artist list does not verify that each track is in Catalan.

## Install

Requirements: Git, Python 3.11 or 3.12, and an internet connection to install dependencies. Run all commands from the repository root. Use a virtual environment to keep dependencies separate.

Windows PowerShell:

```powershell
git clone https://github.com/canmils/catala-music-radar.git
cd catala-music-radar
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS/Linux:

```sh
git clone https://github.com/canmils/catala-music-radar.git
cd catala-music-radar
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Below, `python` means the virtual-environment interpreter: `.\.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux. You can instead activate the environment with `.\.venv\Scripts\Activate.ps1` or `source .venv/bin/activate`. If PowerShell blocks activation, use the direct interpreter path above; activation is optional.


## First use

1. Edit `data/artists.txt`: one artist name per line. Start with one artist, such as `Oques Grasses`, so you can inspect the source result.
2. Run the default, free MusicBrainz collector:

```sh
python src/main.py
```

Expected output: timestamped `musicbrainz_all_*.csv`, `musicbrainz_recent_*.csv`, `musicbrainz_upcoming_*.csv`, `musicbrainz_unknown_date_*.csv`, and `musicbrainz_failed_*.csv` under `output/`. An empty input/result prints an explanatory message. Inspect artist identity and dates before trusting a row.

Optional Spotify: copy `.env.example` to `.env` (`Copy-Item .env.example .env` in PowerShell; `cp .env.example .env` on macOS/Linux), set your developer client ID/secret, edit `data/spotify_playlists.txt`, and run `python src/spotify_playlist_collector.py`. Expected output: `spotify_all_*.csv` and `spotify_recent_*.csv`. Spotify credentials and playlist access are required; no OpenAI key is used.

## Scope, data and limitations

Recent means a full release date within the last 90 days; incomplete dates are classified as unknown. MusicBrainz limits each artist query to 50 release groups, so this is not an exhaustive discography. Ambiguous artist names, API restrictions and missing dates require manual review. Spotify client credentials do not guarantee access to every playlist.

## Update your copy

Stop the application with Ctrl+C. Back up `data/artists.txt`, `data/spotify_playlists.txt`, `.env`, and `output/` locally. Check `git status` first; commit your edits on a branch before pulling if you have changed tracked files.

```sh
git pull --ff-only
python -m pip install -r requirements.txt
```

Use the same virtual-environment interpreter for Python commands. Restart with the run command above. If pulling reports divergent history, resolve your branch changes rather than forcing or discarding work.

## Troubleshooting

- Command not found: install the prerequisite and reopen the terminal.
- Missing module: install dependencies using the same interpreter or package manager that starts the app.
- Missing file: make sure you are in this repository's root directory and have followed the example setup.
- Port already used: stop the earlier server or select another port where supported.
- Provider error: check key, account credit, model access and internet connectivity. Repeating a model request can incur another charge.

## Verify, report bugs and contribute

`python -m compileall -q src`. Run a one-artist lookup and inspect the CSV. Date/URL parsing and mocked source checks do not require network access.

Report bugs at https://github.com/canmils/catala-music-radar/issues with your OS, runtime version, commit (`git rev-parse HEAD`), exact command, sanitized error, and expected versus actual result. Feature requests should describe the user problem and a small example. Do not attach credentials or private company data.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the fork → branch → test → pull-request workflow. Installation checks do not establish commercial value, factual accuracy, or AI output quality.

## License

MIT; see [LICENSE](LICENSE). This covers repository code and authored documentation, not third-party data, trademarks, captured content or your private inputs. Retain dependency and upstream notices.

## Offline onboarding tests

`python -m unittest discover -s tests -v` exercises the first-use path with fictional/mocked input. CI runs this on Ubuntu and Windows; a configured workflow is not proof its remote run has passed. Desktop rendering and external-provider availability require separate checks.

## Verification record

See [ONBOARDING_CHECKS.md](ONBOARDING_CHECKS.md) for checks actually run and limits.
