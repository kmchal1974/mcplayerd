"""Core McPlayerD daemon application."""

from mcplayerd import __version__
from mcplayerd.mpd_client import McPlayerMPDClient


def run() -> None:
    """Start McPlayerD and read the current MPD playback state."""
    print("McPlayerD starting")
    print(f"McPlayerD version {__version__}")

    mpd = McPlayerMPDClient()

    try:
        mpd.connect()
        print("Connected to MPD")

        status = mpd.get_status()
        song = mpd.get_current_song()

        print(f"Playback state: {status.get('state', 'unknown')}")
        print(f"Volume: {status.get('volume', 'unknown')}")

        if song:
            print(f"Artist: {song.get('artist', 'unknown')}")
            print(f"Album: {song.get('album', 'unknown')}")
            print(f"Title: {song.get('title', 'unknown')}")
            print(f"File: {song.get('file', 'unknown')}")
        else:
            print("Current song: none")

    except Exception as exc:
        print(f"MPD error: {exc}")

    finally:
        try:
            mpd.disconnect()
        except Exception:
            pass