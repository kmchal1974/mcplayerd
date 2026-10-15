
"""Bluetooth game controller input for McPlayerD.

Initial test: Stadia A button toggles playback.
"""

import json
import socket

from evdev import InputDevice, ecodes, list_devices


CONTROL_SOCKET = "/run/mcplayer/player-control.sock"


def find_stadia_controller():
    """Find the Stadia controller without hardcoding an event number."""
    for path in list_devices():
        device = InputDevice(path)
        if device.name.startswith("Stadia"):
            return device
        device.close()

    return None


def send_player_command(action):
    """Send a command to McPlayerD's existing player-control socket."""
    request = json.dumps({"action": action}).encode("utf-8")

    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as connection:
        connection.settimeout(3)
        connection.connect(CONTROL_SOCKET)
        connection.sendall(request)
        response = connection.recv(4096)

    result = json.loads(response.decode("utf-8"))

    if not result.get("ok"):
        raise RuntimeError(result.get("error", "Player command failed"))

    return result


def main():
    controller = find_stadia_controller()

    if controller is None:
        print("Stadia controller not found.")
        return

    print(f"Connected to {controller.name}")
    print("Press A to toggle playback. Ctrl+C to exit.")

    try:
        for event in controller.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.code == ecodes.BTN_SOUTH and event.value == 1:
                    try:
                        result = send_player_command("toggle")
                        print(f"Playback: {result['playback']['state']}")
                    except (OSError, ValueError, KeyError, RuntimeError) as exc:
                        print(f"Player control error: {exc}")
    except KeyboardInterrupt:
        print("\nBluetooth controller test stopped.")
    finally:
        controller.close()


if __name__ == "__main__":
    main()
