import re
import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables
load_dotenv()

PLAYLISTS_FILE = Path("data/spotify_playlists.txt")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

DAYS_BACK = 90


def extract_playlist_id(text):
    text = text.strip()

    if "open.spotify.com/playlist/" in text:
        match = re.search(r"playlist/([a-zA-Z0-9]+)", text)
        if match:
            return match.group(1)

    if text.startswith("spotify:playlist:"):
        return text.split(":")[-1]

    return text


def classify_date(release_date, precision, days_back=DAYS_BACK):
    if not release_date:
        return "unknown_date"

    if precision != "day":
        return "unknown_date"

    try:
        parsed = datetime.strptime(release_date, "%Y-%m-%d").date()
    except ValueError:
        return "unknown_date"

    today = datetime.now().date()
    cutoff = today - timedelta(days=days_back)

    if parsed > today:
        return "upcoming"

    if parsed >= cutoff:
        return "recent"

    return "old"


def main():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    	client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    	client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    ))

    playlists = [
        line.strip()
        for line in PLAYLISTS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

    rows = []

    for playlist_raw in playlists:
        playlist_id = extract_playlist_id(playlist_raw)
        print(f"Reading playlist: {playlist_id}")

        playlist = sp.playlist(playlist_id)

        playlist_name = playlist.get("name", "")
        playlist_owner = playlist.get("owner", {}).get("display_name", "")
        playlist_url = playlist.get("external_urls", {}).get("spotify", "")

        results = sp.playlist_items(playlist_id)

        while results:
            items = results.get("items", [])

            for item in items:
                track = item.get("track")
                if not track:
                    continue

                album = track.get("album", {})
                artists = track.get("artists", [])

                artist_names = ", ".join([a.get("name", "") for a in artists])

                release_date = album.get("release_date", "")
                precision = album.get("release_date_precision", "")
                date_status = classify_date(release_date, precision)

                rows.append({
                    "playlist_name": playlist_name,
                    "playlist_owner": playlist_owner,
                    "playlist_url": playlist_url,
                    "track_name": track.get("name", ""),
                    "artist_names": artist_names,
                    "album_name": album.get("name", ""),
                    "release_date": release_date,
                    "date_status": date_status
                })

            if results.get("next"):
                results = sp.next(results)
            else:
                break

    df = pd.DataFrame(rows)

    if df.empty:
        print("No tracks found.")
        return

    df = df.drop_duplicates()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    all_file = OUTPUT_DIR / f"spotify_all_{timestamp}.csv"
    recent_file = OUTPUT_DIR / f"spotify_recent_{timestamp}.csv"

    df.to_csv(all_file, index=False, encoding="utf-8-sig")

    recent_df = df[df["date_status"] == "recent"]
    recent_df.to_csv(recent_file, index=False, encoding="utf-8-sig")

    print("\nDONE")
    print(f"All tracks: {all_file}")
    print(f"Recent tracks: {recent_file}")
    print(f"Total tracks: {len(df)}")
    print(f"Recent tracks: {len(recent_df)}")


if __name__ == "__main__":
    main()