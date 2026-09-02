"""Core McPlayerD daemon application."""

import threading
import time

from mcplayerd import __version__
from mcplayerd.mpd_client import McPlayerMPDClient
from mcplayerd.network_manager import NetworkManagerStatus
from mcplayerd.state_writer import STATE_PATH, write_state

RECONNECT_DELAY = 5
NETWORK_CHECK_INTERVAL = 5
FALLBACK_AP_DELAY = 30
PREFERRED_WIFI_CHECK_INTERVAL = 30
WIFI_SWITCH_COOLDOWN = 60

def wait_for_network_fallback(
    network_manager: NetworkManagerStatus,
) -> None:
    """Manage preferred Wi-Fi selection and fallback AP activation."""
    disconnected_since: float | None = None
    last_preferred_check = 0.0
    last_wifi_switch = 0.0

    while True:
        now = time.monotonic()

        if network_manager.has_usable_wifi():
            disconnected_since = None

            # Periodically see whether another saved Wi-Fi network
            # is meaningfully stronger than the current connection.
            if (
                now - last_preferred_check
                >= PREFERRED_WIFI_CHECK_INTERVAL
                and now - last_wifi_switch >= WIFI_SWITCH_COOLDOWN
            ):
                last_preferred_check = now

                active_connection = (
                    network_manager.get_active_wifi_connection()
                )
                preferred_connection = (
                    network_manager.get_preferred_wifi_connection()
                )

                if (
                    active_connection is not None
                    and preferred_connection is not None
                    and preferred_connection != active_connection
                ):
                    print(
                        "Switching Wi-Fi: "
                        f"{active_connection} -> "
                        f"{preferred_connection}",
                        flush=True,
                    )

                    if network_manager.activate_wifi_connection(
                        preferred_connection
                    ):
                        last_wifi_switch = time.monotonic()

                        print(
                            "Wi-Fi switch successful: "
                            f"{preferred_connection}",
                            flush=True,
                        )
                    else:
                        print(
                            "Wi-Fi switch failed: "
                            f"{preferred_connection}",
                            flush=True,
                        )

        elif network_manager.should_start_fallback_ap():
            if disconnected_since is None:
                disconnected_since = now

                print(
                    "Usable Wi-Fi lost; fallback timer started",
                    flush=True,
                )

            elapsed = now - disconnected_since

            if elapsed >= FALLBACK_AP_DELAY:
                print(
                    "Starting fallback access point",
                    flush=True,
                )

                if network_manager.start_fallback_ap():
                    print(
                        "Fallback access point started",
                        flush=True,
                    )
                else:
                    print(
                        "Fallback access point failed to start",
                        flush=True,
                    )

                return

        time.sleep(NETWORK_CHECK_INTERVAL)


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

    network_thread = threading.Thread(
        target=wait_for_network_fallback,
        args=(network_manager,),
        daemon=True,
        name="network-fallback",
    )
    network_thread.start()

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
    print(
        f"Fallback AP needed: "
        f"{network_manager.should_start_fallback_ap()}",
        flush=True,
    )
    print(
        f"Visible known Wi-Fi: "
        f"{network_manager.get_known_wifi_signals()}",
        flush=True,
    )
    print(
        f"Preferred Wi-Fi connection: "
        f"{network_manager.get_preferred_wifi_connection()}",
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
