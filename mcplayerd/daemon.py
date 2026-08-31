"""Core McPlayerD daemon application."""

from mcplayerd import __version__
from mcplayerd.mpd_client import McPlayerMPDClient


def run() -> None:
    """Start McPlayerD and verify the MPD connection."""
    print("McPlayerD starting")
    print(f"McPlayerD version {__version__}")

    mpd = McPlayerMPDClient()

    try:
        mpd.connect()
        print("Connected to MPD")
    except Exception as exc:
        print(f"MPD connection failed: {exc}")
        return
    finally:
        try:
            mpd.disconnect()
        except Exception:
            pass