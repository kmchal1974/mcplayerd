"""Core McPlayerD daemon application."""

from mcplayerd import __version__
from mcplayerd.mpd_client import McPlayerMPDClient
from mcplayerd.state_writer import STATE_PATH, write_state


def build_state(mpd: McPlayerMPDClient) -> dict:
    """Build a clean McPlayerD state snapshot."""
    status = mpd.get_status()
    song = mpd.get_current_song()

    volume = status.get("volume")

    return {
        "version": __version__,
        "playback": {
            "state": status.get("state", "unknown"),
            "volume": int(volume) if volume is not None else None,
        },
        "song": {
            "artist": song.get("artist") if song else None,
            "album": song.get("album") if song else None,
            "title": song.get("title") if song else None,
            "file": song.get("file") if song else None,
        },
    }


def run() -> None:
    """Start McPlayerD and write the current MPD state."""
    print("McPlayerD starting")
    print(f"McPlayerD version {__version__}")

    mpd = McPlayerMPDClient()

    try:
        mpd.connect()
        print("Connected to MPD")

        state = build_state(mpd)
        write_state(state)

        print(f"State written to {STATE_PATH}")

    except Exception as exc:
        print(f"McPlayerD error: {exc}")

    finally:
        try:
            mpd.disconnect()
        except Exception:
            pass