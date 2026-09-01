"""Read-only NetworkManager support for McPlayerD."""

import os
import shutil
import subprocess


class NetworkManagerStatus:
    """Read basic NetworkManager availability and Wi-Fi state."""

    def __init__(self) -> None:
        self.nmcli_path = shutil.which("nmcli")

    def is_available(self) -> bool:
        """Return True when nmcli is installed."""
        return self.nmcli_path is not None

    def is_running(self) -> bool:
        """Return True when NetworkManager is running."""
        if not self.nmcli_path:
            return False

        env = os.environ.copy()
        env["LC_ALL"] = "C"

        result = subprocess.run(
            [self.nmcli_path, "-t", "-f", "RUNNING", "general"],
            capture_output=True,
            text=True,
            timeout=5,
            env=env,
            check=False,
        )

        return result.returncode == 0 and result.stdout.strip() == "running"

    def get_known_wifi_connections(self) -> list[str]:
        """Return saved NetworkManager Wi-Fi connection names."""
        if not self.nmcli_path:
            return []

        env = os.environ.copy()
        env["LC_ALL"] = "C"

        result = subprocess.run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "NAME,TYPE",
                "connection",
                "show",
            ],
            capture_output=True,
            text=True,
            timeout=5,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            return []

        connections: list[str] = []

        for line in result.stdout.splitlines():
            try:
                name, connection_type = line.rsplit(":", 1)
            except ValueError:
                continue

            if connection_type == "802-11-wireless":
                connections.append(name)

        return connections

    def get_active_wifi_connection(self) -> str | None:
        """Return the active NetworkManager Wi-Fi connection name."""
        if not self.nmcli_path:
            return None

        env = os.environ.copy()
        env["LC_ALL"] = "C"

        result = subprocess.run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "NAME,TYPE",
                "connection",
                "show",
                "--active",
            ],
            capture_output=True,
            text=True,
            timeout=5,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():
            try:
                name, connection_type = line.rsplit(":", 1)
            except ValueError:
                continue

            if connection_type == "802-11-wireless":
                return name

        return None

    def get_active_wifi_ssid(self) -> str | None:
        """Return the SSID currently used by the Wi-Fi interface."""
        if not self.nmcli_path:
            return None

        env = os.environ.copy()
        env["LC_ALL"] = "C"

        result = subprocess.run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "ACTIVE,SSID",
                "device",
                "wifi",
            ],
            capture_output=True,
            text=True,
            timeout=5,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():
            if line.startswith("yes:"):
                return line[4:] or None

        return None

    def get_wifi_device(self) -> str | None:
        """Return the NetworkManager Wi-Fi device name."""
        if not self.nmcli_path:
            return None

        env = os.environ.copy()
        env["LC_ALL"] = "C"

        result = subprocess.run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "DEVICE,TYPE",
                "device",
                "status",
            ],
            capture_output=True,
            text=True,
            timeout=5,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():
            try:
                device, device_type = line.rsplit(":", 1)
            except ValueError:
                continue

            if device_type == "wifi":
                return device

        return None

    def get_wifi_device_state(self) -> str | None:
        """Return the NetworkManager state of the Wi-Fi device."""
        if not self.nmcli_path:
            return None

        env = os.environ.copy()
        env["LC_ALL"] = "C"

        result = subprocess.run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "DEVICE,TYPE,STATE",
                "device",
                "status",
            ],
            capture_output=True,
            text=True,
            timeout=5,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():
            parts = line.rsplit(":", 2)

            if len(parts) != 3:
                continue

            device, device_type, state = parts

            if device_type == "wifi":
                return state

        return None
