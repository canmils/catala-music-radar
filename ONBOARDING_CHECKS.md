# Verification record

## 15 October 2026

- Offline tests pass on Python 3.12: CSV creation from a mocked MusicBrainz response, empty artist list, and a User-Agent that meets the MusicBrainz policy.
- User-Agent changed to `catala-music-radar/0.5 ( https://github.com/canmils/catala-music-radar )`, the format MusicBrainz asks for. The previous value had no real contact.
- The 1.5-second pause between requests stays under the MusicBrainz limit of about one request per second.

## Not checked

- A live MusicBrainz run (not reachable from the editing environment).
- Spotify access.
