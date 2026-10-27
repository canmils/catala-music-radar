# Catalan Music Radar

Finds recent and upcoming releases from a list of Catalan artists you choose,
using the free MusicBrainz API, and writes CSV files. Free, no API key needed.

## Commands

- Install: `python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt`
- Run: `.venv/bin/python src/main.py`
- Tests: `.venv/bin/python -m unittest discover -s tests -v`

## Layout

- `src/main.py`, `src/musicbrainz_collector.py`, `src/spotify_playlist_collector.py` (optional).
- `data/`: artist list and outputs. `tests/`.

## Rules

- Respect MusicBrainz rate limits and its user agent rules.
- The core must work without any key. Never commit `.env`.

## Coding discipline (Karpathy guidelines)

Before writing, reviewing or refactoring code, load the `karpathy-guidelines` skill
(source: github.com/multica-ai/andrej-karpathy-skills, MIT). The short version:

1. **Read first.** Read the code, docs and tests you will touch before you change anything. Investigate; do not guess.
2. **Think before coding.** State your assumptions. If there is more than one reading of the task, name them. If something is unclear, stop and ask.
3. **Simplicity first.** Write the minimum code for the request. No speculative features, no early abstractions, no new dependency without a stated reason.
4. **Surgical changes.** Touch only what the task needs and match the existing style. Mention unrelated problems; do not fix them silently.
5. **Define success before building.** Turn the task into a check, for example a test that fails first and then passes.
6. **Test the behaviour and fix the root cause.** A green build is not enough. Do not patch symptoms.
7. **Explain what changed and why.** Files touched, the reason, and the checks you actually ran.
