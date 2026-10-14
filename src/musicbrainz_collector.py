import requests
import time
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

ARTISTS_FILE = Path("data/artists.txt")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

DAYS_BACK = 90
REQUEST_SLEEP = 1.5
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": "catala-music-radar/0.4 (local personal project; contact: local)"
}


def normalize(text):
    return text.lower().strip()


def safe_get(url, params):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(url, params=params, headers=HEADERS, timeout=30)

            if r.status_code in [500, 502, 503, 504, 429]:
                wait = attempt * 3
                print(f"Temporary error {r.status_code}. Retry {attempt}/{MAX_RETRIES}. Waiting {wait}s...")
                time.sleep(wait)
                continue

            r.raise_for_status()
            return r.json()

        except requests.exceptions.RequestException as e:
            wait = attempt * 3
            print(f"Request error: {e}. Retry {attempt}/{MAX_RETRIES}. Waiting {wait}s...")
            time.sleep(wait)

    return None


def search_artist(artist_name):
    url = "https://musicbrainz.org/ws/2/artist/"
    params = {
        "query": f'artist:"{artist_name}"',
        "fmt": "json",
        "limit": 5
    }

    data = safe_get(url, params)
    if not data:
        return None

    artists = data.get("artists", [])

    for artist in artists:
        if normalize(artist.get("name", "")) == normalize(artist_name):
            return artist

    return None


def get_releases(artist_id):
    url = "https://musicbrainz.org/ws/2/release-group/"
    params = {
        "artist": artist_id,
        "fmt": "json",
        "limit": 50,
        "type": "album|single|ep"
    }

    data = safe_get(url, params)
    if not data:
        return None

    return data.get("release-groups", [])


def parse_release_date(date_text):
    if not date_text or len(date_text) < 10:
        return None

    try:
        return datetime.strptime(date_text[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def classify_date(date_text, days_back=DAYS_BACK):
    release_date = parse_release_date(date_text)

    if release_date is None:
        return "unknown_date"

    today = datetime.now().date()
    cutoff = today - timedelta(days=days_back)

    if release_date > today:
        return "upcoming"

    if release_date >= cutoff:
        return "recent"

    return "old"


def main():
    artists = [
        line.strip()
        for line in ARTISTS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    rows = []

    for index, artist_name in enumerate(artists, start=1):
        print(f"[{index}/{len(artists)}] Searching artist: {artist_name}")

        artist = search_artist(artist_name)
        time.sleep(REQUEST_SLEEP)

        if not artist:
            rows.append({
                "artist_input": artist_name,
                "artist_found": "",
                "artist_id": "",
                "release_title": "",
                "release_date": "",
                "release_type": "",
                "source": "MusicBrainz",
                "status": "artist_not_found_or_request_failed",
                "date_status": "unknown_date"
            })
            continue

        releases = get_releases(artist["id"])
        time.sleep(REQUEST_SLEEP)

        if releases is None:
            rows.append({
                "artist_input": artist_name,
                "artist_found": artist.get("name", ""),
                "artist_id": artist.get("id", ""),
                "release_title": "",
                "release_date": "",
                "release_type": "",
                "source": "MusicBrainz",
                "status": "release_request_failed",
                "date_status": "unknown_date"
            })
            continue

        if not releases:
            rows.append({
                "artist_input": artist_name,
                "artist_found": artist.get("name", ""),
                "artist_id": artist.get("id", ""),
                "release_title": "",
                "release_date": "",
                "release_type": "",
                "source": "MusicBrainz",
                "status": "no_releases_found",
                "date_status": "unknown_date"
            })
            continue

        for release in releases:
            release_date = release.get("first-release-date", "")
            date_status = classify_date(release_date)

            rows.append({
                "artist_input": artist_name,
                "artist_found": artist.get("name", ""),
                "artist_id": artist.get("id", ""),
                "release_title": release.get("title", ""),
                "release_date": release_date,
                "release_type": release.get("primary-type", ""),
                "source": "MusicBrainz",
                "status": "ok",
                "date_status": date_status
            })

    if not rows:
        print("No artists or release records found. Check data/artists.txt and the source responses.")
        return
    df = pd.DataFrame(rows)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    all_file = OUTPUT_DIR / f"musicbrainz_all_{timestamp}.csv"
    recent_file = OUTPUT_DIR / f"musicbrainz_recent_{timestamp}.csv"
    upcoming_file = OUTPUT_DIR / f"musicbrainz_upcoming_{timestamp}.csv"
    unknown_file = OUTPUT_DIR / f"musicbrainz_unknown_date_{timestamp}.csv"
    failed_file = OUTPUT_DIR / f"musicbrainz_failed_{timestamp}.csv"

    df.to_csv(all_file, index=False, encoding="utf-8-sig")

    df[df["date_status"] == "recent"].to_csv(recent_file, index=False, encoding="utf-8-sig")
    df[df["date_status"] == "upcoming"].to_csv(upcoming_file, index=False, encoding="utf-8-sig")
    df[df["date_status"] == "unknown_date"].to_csv(unknown_file, index=False, encoding="utf-8-sig")
    df[df["status"].str.contains("failed|not_found", case=False, na=False)].to_csv(
        failed_file, index=False, encoding="utf-8-sig"
    )

    print("\nDONE")
    print(f"All output: {all_file}")
    print(f"Recent output: {recent_file}")
    print(f"Upcoming output: {upcoming_file}")
    print(f"Unknown-date output: {unknown_file}")
    print(f"Failed output: {failed_file}")
    print(f"All rows: {len(df)}")
    print(f"Recent rows: {len(df[df['date_status'] == 'recent'])}")
    print(f"Upcoming rows: {len(df[df['date_status'] == 'upcoming'])}")
    print(f"Failed rows: {len(df[df['status'].str.contains('failed|not_found', case=False, na=False)])}")


if __name__ == "__main__":
    main()