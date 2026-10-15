# Catalan Music Radar

**Find recent and upcoming releases from a list of Catalan artists you choose. Free, no API key.**

You keep a list of artists in a text file. The tool asks [MusicBrainz](https://musicbrainz.org) (a free, open music database) for each artist's releases and writes CSV files: what came out in the last 90 days, what is announced, and what has no full date.

| You give | You get |
| --- | --- |
| `data/artists.txt`, one artist per line | CSV files in `output/`: recent, upcoming, unknown date, all releases, and failed (artist not found or request failed) |

## Run it

Requires Git and Python 3.11 or 3.12.

Windows PowerShell:

```powershell
git clone https://github.com/canmils/catala-music-radar.git
cd catala-music-radar
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py
```

macOS/Linux:

```sh
git clone https://github.com/canmils/catala-music-radar.git
cd catala-music-radar
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/main.py
```

The bundled list has about 60 artists. MusicBrainz allows about one request per second, so a full run takes a few minutes. To try it quickly, keep two or three names in `data/artists.txt` first.

Open `output/musicbrainz_recent_<date>.csv` in Excel or any spreadsheet app.

## Limits

- **Being on your list does not make a song Catalan.** The tool trusts your list. It does not check the language.
- **Names must match exactly** (case does not matter). A spelling difference means "not found": check the failed CSV. If two artists share a name, the tool takes the first one MusicBrainz returns, so check results that look wrong.
- **Not a full discography.** At most 50 release groups per artist.
- **"Recent" needs a full date.** Releases with only a year or month go to the unknown-date file.
- MusicBrainz is community-maintained, so new releases can appear late or be missing.

## Optional: Spotify playlists

`src/spotify_playlist_collector.py` reads tracks from public Spotify playlists listed in `data/spotify_playlists.txt`. It needs your own free Spotify developer credentials: copy `.env.example` to `.env` and fill in `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`. Spotify does not give access to every playlist.

## Tests

```sh
python -m unittest discover -s tests -v
```

Offline, with a mocked MusicBrainz. CI runs them on Ubuntu and Windows.

## Contributing

Issues and pull requests are welcome, especially artist list additions and fixes for wrong artist matches. See [CONTRIBUTING.md](CONTRIBUTING.md). MIT licensed, see [LICENSE](LICENSE).
