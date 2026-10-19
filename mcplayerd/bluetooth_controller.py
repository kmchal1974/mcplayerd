
"""Bluetooth Stadia game controller input for McPlayerD.

Controls:
    A           Play/Pause
    D-pad Left  Previous track
    D-pad Right Next track
    D-pad Up    Volume +5
    D-pad Down  Volume -5

The listener waits for the controller and recovers when its
Linux input device disappears and later returns.
"""

import json
import select
import socket
import time

from evdev import InputDevice, ecodes, list_devices

from mcplayerd.mpd_client import McPlayerMPDClient


CONTROL_SOCKET = "/run/mcplayer/player-control.sock"
VOLUME_STEP = 5
RECONNECT_DELAY = 3
INPUT_POLL_INTERVAL = 1


def find_stadia_controller():
    """Find an available Stadia input device."""
    for path in list_devices():
        try:
            device = InputDevice(path)
        except OSError:
            continue

        if device.name.startswith("Stadia"):
            return device

        device.close()

    return None


def send_player_command(action, value=None):
    """Send a command through McPlayerD's player-control socket."""
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
    """Read MPD volume without changing playback."""
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
    """Adjust volume by one step, limited to 0-100."""
    current_volume = get_current_volume()
    new_volume = max(
        0,
        min(100, current_volume + direction * VOLUME_STEP),
    )

    if new_volume == current_volume:
        print(f"Volume already at {current_volume}%", flush=True)
        return

    result = send_player_command("volume", new_volume)
    actual_volume = result["playback"]["volume"]
    print(f"Volume: {actual_volume}%", flush=True)


def get_controller_action(event):
    """Translate Stadia input events into player actions."""
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


def handle_controller_event(event):
    """Execute a supported Stadia controller command."""
    action = get_controller_action(event)

    if action is None:
        return

    try:
        if action == "volume_up":
            change_volume(1)

        elif action == "volume_down":
            change_volume(-1)

        else:
            result = send_player_command(action)
            print(f"Controller command: {action}", flush=True)

            if action == "toggle":
                print(
                    f"Playback: {result['playback']['state']}",
                    flush=True,
                )

    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        print(f"Player control error: {exc}", flush=True)


def listen_to_controller(controller):
    """Process events until the controller disappears."""
    print(f"Connected to {controller.name}", flush=True)

    while True:
        readable, _, _ = select.select(
            [controller],
            [],
            [],
            INPUT_POLL_INTERVAL,
        )

        if not readable:
            # Detect device removal even when no buttons are pressed.
            if controller.path not in find_matching_devices():
                raise OSError("Stadia input device disappeared")
            continue

        for event in controller.read():
            handle_controller_event(event)



def find_matching_devices():
    """Return paths of currently available Stadia input devices."""
    paths = []

    for path in list_devices():
        try:
            device = InputDevice(path)
        except OSError:
            continue

        try:
            if device.name.startswith("Stadia"):
                paths.append(path)
        finally:
            device.close()

    return paths


def main():
    """Continuously wait for and listen to the Stadia controller."""
    print("McPlayerD Bluetooth controller listener starting", flush=True)

    while True:
        controller = find_stadia_controller()

        if controller is None:
            time.sleep(RECONNECT_DELAY)
            continue

        try:
            listen_to_controller(controller)

        except OSError as exc:
            print(f"Controller disconnected: {exc}", flush=True)

        finally:
            controller.close()

        time.sleep(RECONNECT_DELAY)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBluetooth controller listener stopped.")
