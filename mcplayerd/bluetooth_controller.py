
"""Bluetooth Stadia game controller input for McPlayerD.

Controls:
    A           Play/Pause
    D-pad Left  Previous track
    D-pad Right Next track
    D-pad Up    Volume +5
    D-pad Down  Volume -5

The listener detects controller input devices and attempts limited
HID recovery when BlueZ reports a connected controller without one.
"""

import json
import select
import socket
import subprocess
import time

from evdev import InputDevice, ecodes, list_devices

from mcplayerd.mpd_client import McPlayerMPDClient


CONTROL_SOCKET = "/run/mcplayer/player-control.sock"
VOLUME_STEP = 5
RECONNECT_DELAY = 3
INPUT_POLL_INTERVAL = 1

STADIA_DBUS_PATH = "/org/bluez/hci0/dev_CA_1C_4C_FE_19_FD"
HID_GRACE_PERIOD = 15
RECOVERY_COOLDOWN = 30
MAX_RECOVERY_ATTEMPTS = 2
DBUS_TIMEOUT = 12


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
            if controller.path not in find_matching_devices():
                raise OSError("Stadia input device disappeared")
            continue

        for event in controller.read():
            handle_controller_event(event)


def dbus_device_call(method):
    """Call a BlueZ device method with a bounded timeout."""
    command = [
        "busctl",
        "--allow-interactive-authorization=no",
        "--timeout=10s",
        "call",
        "org.bluez",
        STADIA_DBUS_PATH,
        "org.bluez.Device1",
        method,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=DBUS_TIMEOUT,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"Bluetooth D-Bus {method} failed: {exc}", flush=True)
        return False

    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        print(f"Bluetooth D-Bus {method} failed: {message}", flush=True)
        return False

    return True


def bluez_controller_connected():
    """Check whether BlueZ reports the Stadia controller connected."""
    command = [
        "busctl",
        "--allow-interactive-authorization=no",
        "--timeout=5s",
        "get-property",
        "org.bluez",
        STADIA_DBUS_PATH,
        "org.bluez.Device1",
        "Connected",
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=7,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"Bluetooth status check failed: {exc}", flush=True)
        return False

    if result.returncode != 0:
        return False

    return result.stdout.strip() == "b true"


def recover_stadia_hid():
    """Attempt to recreate a missing Stadia HID input device."""
    print("Stadia HID missing; attempting Bluetooth recovery", flush=True)

    if not dbus_device_call("Disconnect"):
        return False

    time.sleep(2)

    if not dbus_device_call("Connect"):
        return False

    print("Stadia Bluetooth reconnect requested", flush=True)
    return True


def main():
    """Listen for the Stadia controller and recover missing HID input."""
    print("McPlayerD Bluetooth controller listener starting", flush=True)

    missing_since = None
    last_recovery = None
    recovery_attempts = 0

    while True:
        controller = find_stadia_controller()

        if controller is not None:
            missing_since = None
            last_recovery = None
            recovery_attempts = 0

            try:
                listen_to_controller(controller)
            except (OSError, ValueError) as exc:
                print(f"Controller disconnected: {exc}", flush=True)
            finally:
                controller.close()

            time.sleep(RECONNECT_DELAY)
            continue

        if not bluez_controller_connected():
            missing_since = None
            time.sleep(RECONNECT_DELAY)
            continue

        now = time.monotonic()

        if missing_since is None:
            missing_since = now
            print(
                "Stadia connected in BlueZ; waiting for HID input",
                flush=True,
            )

        grace_elapsed = now - missing_since >= HID_GRACE_PERIOD
        cooldown_elapsed = (
            last_recovery is None
            or now - last_recovery >= RECOVERY_COOLDOWN
        )

        if (
            grace_elapsed
            and cooldown_elapsed
            and recovery_attempts < MAX_RECOVERY_ATTEMPTS
        ):
            recovery_attempts += 1
            last_recovery = now

            print(
                f"Stadia HID recovery attempt "
                f"{recovery_attempts}/{MAX_RECOVERY_ATTEMPTS}",
                flush=True,
            )
            recover_stadia_hid()

        elif (
            grace_elapsed
            and recovery_attempts >= MAX_RECOVERY_ATTEMPTS
        ):
            # Avoid repeating this warning every three seconds.
            if recovery_attempts == MAX_RECOVERY_ATTEMPTS:
                print(
                    "Stadia HID recovery limit reached; "
                    "waiting for controller state to change",
                    flush=True,
                )
                recovery_attempts += 1

        time.sleep(RECONNECT_DELAY)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBluetooth controller listener stopped.")
