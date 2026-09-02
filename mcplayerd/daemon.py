"""Core McPlayerD daemon application."""

import time

from mcplayerd import __version__
from mcplayerd.mpd_client import McPlayerMPDClient
from mcplayerd.network_manager import NetworkManagerStatus
from mcplayerd.state_writer import STATE_PATH, write_state

RECONNECT_DELAY = 5


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


def update_state(mpd: McPlayerMPDClient) -> None:
    """Read MPD and write the latest McPlayerD state."""
    state = build_state(mpd)
    write_state(state)
    print(f"State updated: {STATE_PATH}", flush=True)


def run() -> None:
    """Run McPlayerD continuously."""
    print("McPlayerD starting", flush=True)
    print(f"McPlayerD version {__version__}", flush=True)

    network_manager = NetworkManagerStatus()
    print(
        f"NetworkManager available: {network_manager.is_available()}",
        flush=True,
    )
    print(
        f"NetworkManager running: {network_manager.is_running()}",
        flush=True,
    )
    print(
        f"Active Wi-Fi connection: "
        f"{network_manager.get_active_wifi_connection()}",
        flush=True,
    )
    print(
        f"Active Wi-Fi SSID: "
        f"{network_manager.get_active_wifi_ssid()}",
        flush=True,
    )
    print(
        f"Known Wi-Fi connections: "
        f"{network_manager.get_known_wifi_connections()}",
        flush=True,
    )
    print(
        f"Usable Wi-Fi: {network_manager.has_usable_wifi()}",
        flush=True,
    )
    print(
        f"Wi-Fi device: {network_manager.get_wifi_device()}",
        flush=True,
    )
    print(
        f"Wi-Fi device state: "
        f"{network_manager.get_wifi_device_state()}",
        flush=True,
    )

    while True:
        mpd = McPlayerMPDClient()
        try:
            mpd.connect()
            print("Connected to MPD", flush=True)
            update_state(mpd)

            while True:
                changes = mpd.wait_for_change()
                print(
                    f"MPD change detected: {', '.join(changes)}",
                    flush=True,
                )
                update_state(mpd)

        except KeyboardInterrupt:
            print("McPlayerD stopped", flush=True)
            return
        except Exception as exc:
            print(f"MPD connection error: {exc}", flush=True)
            print(
                f"Retrying in {RECONNECT_DELAY} seconds",
                flush=True,
            )
            time.sleep(RECONNECT_DELAY)
        finally:
            try:
                mpd.disconnect()
            except Exception:
                pass
            