
"""Bluetooth Stadia game controller input for McPlayerD.

Controls:
    A           Play/Pause
    D-pad Left  Previous track
    D-pad Right Next track
    D-pad Up    Volume +5
    D-pad Down  Volume -5
"""

import json
import socket

from evdev import InputDevice, ecodes, list_devices

from mcplayerd.mpd_client import McPlayerMPDClient


CONTROL_SOCKET = "/run/mcplayer/player-control.sock"
VOLUME_STEP = 5


def find_stadia_controller():
    """Find the Stadia controller without hardcoding an event number."""
    for path in list_devices():
        device = InputDevice(path)
        if device.name.startswith("Stadia"):
            return device
        device.close()

    return None


def send_player_command(action, value=None):
    """Send a command to McPlayerD's existing player-control socket."""
    request = {"action": action}

    if value is not None:
        request["value"] = value

    payload = json.dumps(request).encode("utf-8")

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(3)
        connection.connect(CONTROL_SOCKET)
        connection.sendall(payload)
        response = connection.recv(4096)

    result = json.loads(response.decode("utf-8"))

    if not result.get("ok"):
        raise RuntimeError(result.get("error", "Player command failed"))

    return result


def get_current_volume():
    """Read the current MPD volume without changing playback."""
    mpd = McPlayerMPDClient()

    try:
        mpd.connect()
        status = mpd.get_status()
        volume = status.get("volume")

        if volume is None:
            raise RuntimeError("MPD did not report a volume level")

        volume = int(volume)

        if not 0 <= volume <= 100:
            raise RuntimeError(f"Invalid MPD volume: {volume}")

        return volume
    finally:
        try:
            mpd.disconnect()
        except Exception:
            pass


def change_volume(direction):
    """Adjust volume by one step, staying within 0-100."""
    current_volume = get_current_volume()
    new_volume = max(
        0,
        min(100, current_volume + direction * VOLUME_STEP),
    )

    if new_volume == current_volume:
        print(f"Volume already at {current_volume}%")
        return

    result = send_player_command("volume", new_volume)
    actual_volume = result["playback"]["volume"]
    print(f"Volume: {actual_volume}%")


def get_controller_action(event):
    """Translate Stadia controller events into player actions."""

    if event.type == ecodes.EV_KEY:
        if event.code == ecodes.BTN_SOUTH and event.value == 1:
            return "toggle"

    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_HAT0X:
            if event.value == -1:
                return "previous"
            if event.value == 1:
                return "next"

        if event.code == ecodes.ABS_HAT0Y:
            if event.value == -1:
                return "volume_up"
            if event.value == 1:
                return "volume_down"

    return None


def main():
    controller = find_stadia_controller()

    if controller is None:
        print("Stadia controller not found.")
        return

    print(f"Connected to {controller.name}")
    print("A: Play/Pause")
    print("D-pad Left/Right: Previous/Next")
    print("D-pad Up/Down: Volume Up/Down")
    print("Press Ctrl+C to exit.")

    try:
        for event in controller.read_loop():
            action = get_controller_action(event)

            if action is None:
                continue

            try:
                if action == "volume_up":
                    change_volume(1)

                elif action == "volume_down":
                    change_volume(-1)

                else:
                    result = send_player_command(action)
                    print(f"Controller command: {action}")

                    if action == "toggle":
                        print(
                            f"Playback: {result['playback']['state']}"
                        )

            except (
                OSError,
                ValueError,
                KeyError,
                RuntimeError,
            ) as exc:
                print(f"Player control error: {exc}")

    except KeyboardInterrupt:
        print("\nBluetooth controller test stopped.")

    finally:
        controller.close()


if __name__ == "__main__":
    main()
