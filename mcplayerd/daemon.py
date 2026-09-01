"""Core McPlayerD daemon application."""

from mcplayerd import __version__
from mcplayerd.mpd_client import McPlayerMPDClient


def print_state(mpd: McPlayerMPDClient) -> None:
    """Print the current MPD playback state."""
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


def run() -> None:
    """Start McPlayerD and wait for one MPD change."""
    print("McPlayerD starting")
    print(f"McPlayerD version {__version__}")

    mpd = McPlayerMPDClient()

    try:
        mpd.connect()
        print("Connected to MPD")

        print("\nCurrent state:")
        print_state(mpd)

        print("\nWaiting for MPD change...")

        changes = mpd.wait_for_change()

        print(f"Change detected: {', '.join(changes)}")

        print("\nUpdated state:")
        print_state(mpd)

    except KeyboardInterrupt:
        print("\nMcPlayerD stopped")

    except Exception as exc:
        print(f"MPD error: {exc}")

    finally:
        try:
            mpd.disconnect()
        except Exception:
            pass