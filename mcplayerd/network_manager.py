"""Read-only NetworkManager support for McPlayerD."""

import os
import tempfile
import shutil
import subprocess


class NetworkManagerStatus:
    """Read basic NetworkManager availability and Wi-Fi state."""

    def __init__(self) -> None:
        self.nmcli_path = shutil.which("nmcli")

    def _environment(self) -> dict[str, str]:
        """Return a predictable environment for nmcli output."""
        env = os.environ.copy()
        env["LC_ALL"] = "C"
        return env

    def is_available(self) -> bool:
        """Return True when nmcli is installed."""
        return self.nmcli_path is not None

    def is_running(self) -> bool:
        """Return True when NetworkManager is running."""
        if not self.nmcli_path:
            return False

        result = subprocess.run(
            [self.nmcli_path, "-t", "-f", "RUNNING", "general"],
            capture_output=True,
            text=True,
            timeout=5,
            env=self._environment(),
            check=False,
        )

        return result.returncode == 0 and result.stdout.strip() == "running"

    def get_active_wifi_connection(self) -> str | None:
        """Return the active NetworkManager Wi-Fi connection name."""
        if not self.nmcli_path:
            return None

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
            env=self._environment(),
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
            env=self._environment(),
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
            env=self._environment(),
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
            env=self._environment(),
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

    def get_known_wifi_connections(self) -> list[str]:
        """Return saved NetworkManager Wi-Fi connection names."""
        if not self.nmcli_path:
            return []

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
            env=self._environment(),
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

    def has_usable_wifi(
        self,
        hotspot_connection: str = "McPlayer-AP",
    ) -> bool:
        """Return True when connected to a normal Wi-Fi network."""
        if not self.is_running():
            return False

        connection = self.get_active_wifi_connection()
        state = self.get_wifi_device_state()

        if connection is None:
            return False

        if connection == hotspot_connection:
            return False

        return state == "connected"

    def should_start_fallback_ap(
        self,
        hotspot_connection: str = "McPlayer-AP",
    ) -> bool:
        """Return True when McPlayer should use its fallback access point."""
        if not self.is_available():
            return False

        if not self.is_running():
            return False

        active_connection = self.get_active_wifi_connection()
        wifi_state = self.get_wifi_device_state()

        if active_connection == hotspot_connection:
            return False

        if active_connection is None:
            return True

        if wifi_state != "connected":
            return True

        if not self.has_usable_wifi(hotspot_connection):
            return True

        return False

    def start_fallback_ap(
        self,
        hotspot_connection: str = "McPlayer-AP",
    ) -> bool:
        """Activate the existing fallback access-point profile."""
        if not self.nmcli_path:
            return False

        result = subprocess.run(
            [
                self.nmcli_path,
                "--wait",
                "15",
                "connection",
                "up",
                "id",
                hotspot_connection,
                "ifname",
                "wlan0",
            ],
            capture_output=True,
            text=True,
            timeout=20,
            env=self._environment(),
            check=False,
        )

        return result.returncode == 0

    def get_known_wifi_signals(
        self,
        hotspot_connection: str = "McPlayer-AP",
    ) -> list[dict]:
        """Return visible saved Wi-Fi networks and their signal strength."""
        if not self.nmcli_path or not self.is_running():
            return []

        env = self._environment()

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

        known_networks: dict[str, str] = {}

        for line in result.stdout.splitlines():
            try:
                name, connection_type = line.rsplit(":", 1)
            except ValueError:
                continue

            if (
                connection_type != "802-11-wireless"
                or name == hotspot_connection
            ):
                continue

            ssid_result = subprocess.run(
                [
                    self.nmcli_path,
                    "-g",
                    "802-11-wireless.ssid",
                    "connection",
                    "show",
                    name,
                ],
                capture_output=True,
                text=True,
                timeout=5,
                env=env,
                check=False,
            )

            if ssid_result.returncode == 0:
                ssid = ssid_result.stdout.strip()

                if ssid:
                    known_networks[ssid] = name

        subprocess.run(
            [
                self.nmcli_path,
                "device",
                "wifi",
                "rescan",
                "ifname",
                "wlan0",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            env=env,
            check=False,
        )

        result = subprocess.run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "SSID,SIGNAL",
                "device",
                "wifi",
                "list",
                "--rescan",
                "yes",
            ],
            capture_output=True,
            text=True,
            timeout=15,
            env=env,
            check=False,
        )

        if result.returncode != 0:
            return []

        visible: dict[str, int] = {}

        for line in result.stdout.splitlines():
            try:
                ssid, signal_text = line.rsplit(":", 1)
                signal = int(signal_text)
            except (ValueError, TypeError):
                continue

            if ssid in known_networks:
                visible[ssid] = max(
                    signal,
                    visible.get(ssid, 0),
                )

        networks = [
            {
                "connection": known_networks[ssid],
                "ssid": ssid,
                "signal": signal,
            }
            for ssid, signal in visible.items()
        ]

        return sorted(
            networks,
            key=lambda network: network["signal"],
            reverse=True,
        )

    def get_preferred_wifi_connection(
        self,
        hotspot_connection: str = "McPlayer-AP",
        switch_margin: int = 15,
    ) -> str | None:
        """Return the preferred saved Wi-Fi connection based on signal strength."""
        networks = self.get_known_wifi_signals(hotspot_connection)
        if not networks:
            return None
        active_connection = self.get_active_wifi_connection()
        if active_connection is None or active_connection == hotspot_connection:
            return networks[0]["connection"]
        current_network = next(
            (
                network
                for network in networks
                if network["connection"] == active_connection
            ),
            None,
        )
        best_network = networks[0]
        if current_network is None:
            return best_network["connection"]
        if best_network["connection"] == active_connection:
            return active_connection
        if best_network["signal"] >= current_network["signal"] + switch_margin:
            return best_network["connection"]
        return active_connection

    def get_preferred_wifi_connection(
        self,
        hotspot_connection: str = "McPlayer-AP",
        switch_margin: int = 15,
    ) -> str | None:
        """Return the preferred saved Wi-Fi connection based on signal strength."""
        networks = self.get_known_wifi_signals(hotspot_connection)

        if not networks:
            return None

        active_connection = self.get_active_wifi_connection()

        if active_connection is None or active_connection == hotspot_connection:
            return networks[0]["connection"]

        current_network = next(
            (
                network
                for network in networks
                if network["connection"] == active_connection
            ),
            None,
        )

        best_network = networks[0]

        if current_network is None:
            return best_network["connection"]

        if best_network["connection"] == active_connection:
            return active_connection

        if best_network["signal"] >= current_network["signal"] + switch_margin:
            return best_network["connection"]

        return active_connection

    def activate_wifi_connection(
        self,
        connection_name: str,
    ) -> bool:
        """Activate a saved Wi-Fi connection on the Wi-Fi device."""
        if not self.nmcli_path:
            return False

        wifi_device = self.get_wifi_device()

        if wifi_device is None:
            return False

        result = subprocess.run(
            [
                self.nmcli_path,
                "--wait",
                "20",
                "connection",
                "up",
                "id",
                connection_name,
                "ifname",
                wifi_device,
            ],
            capture_output=True,
            text=True,
            timeout=25,
            env=self._environment(),
            check=False,
        )

        return result.returncode == 0

    def try_saved_wifi_connections(
        self,
        hotspot_connection: str = "McPlayer-AP",
    ) -> str | None:
        """Try saved normal Wi-Fi profiles and return the first that connects."""
        connections = self.get_known_wifi_connections()

        for connection in connections:
            if connection == hotspot_connection:
                continue

            if self.activate_wifi_connection(connection):
                return connection

        return None

    def add_wifi_connection(
        self,
        ssid: str,
        password: str,
    ) -> bool:
        """Create, save, and activate a WPA/WPA2 Wi-Fi connection."""

        if not self.nmcli_path:
            return False

        wifi_device = self.get_wifi_device()

        if wifi_device is None:
            return False

        ssid = ssid.strip()

        if not ssid or not password:
            return False

        # Do not create a duplicate saved profile.
        if ssid in self.get_known_wifi_connections():
            return self.activate_wifi_connection(ssid)

        create_result = subprocess.run(
            [
                self.nmcli_path,
                "connection",
                "add",
                "type",
                "wifi",
                "ifname",
                wifi_device,
                "con-name",
                ssid,
                "ssid",
                ssid,
                "wifi-sec.key-mgmt",
                "wpa-psk",
            ],
            capture_output=True,
            text=True,
            timeout=15,
            env=self._environment(),
            check=False,
        )

        if create_result.returncode != 0:
            return False

        password_file = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                prefix="mcplayer-wifi-",
                delete=False,
            ) as temp_file:
                password_file = temp_file.name

                temp_file.write(
                    "802-11-wireless-security.psk:"
                    + password
                    + "\n"
                )

            os.chmod(
                password_file,
                0o600,
            )

            connect_result = subprocess.run(
                [
                    self.nmcli_path,
                    "--wait",
                    "60",
                    "connection",
                    "up",
                    "id",
                    ssid,
                    "ifname",
                    wifi_device,
                    "passwd-file",
                    password_file,
                ],
                capture_output=True,
                text=True,
                timeout=65,
                env=self._environment(),
                check=False,
            )

            if connect_result.returncode == 0:
                return True

            # Remove the incomplete profile if connection failed.
            subprocess.run(
                [
                    self.nmcli_path,
                    "connection",
                    "delete",
                    "id",
                    ssid,
                ],
                capture_output=True,
                text=True,
                timeout=15,
                env=self._environment(),
                check=False,
            )

            return False
        finally:
            if password_file is not None:
                try:
                    os.remove(password_file)
                except FileNotFoundError:
                    pass

    def scan_wifi_networks(self) -> list[dict]:
        """Scan for nearby Wi-Fi networks."""

        if not self.nmcli_path:
            return []

        wifi_device = self.get_wifi_device()

        if wifi_device is None:
            return []

        result = subprocess.run(
            [
                self.nmcli_path,
                "-t",
                "-f",
                "SSID,SIGNAL,SECURITY",
                "device",
                "wifi",
                "list",
                "ifname",
                wifi_device,
                "--rescan",
                "yes",
            ],
            capture_output=True,
            text=True,
            timeout=20,
            env=self._environment(),
            check=False,
        )

        if result.returncode != 0:
            return []

        networks = {}

        for line in result.stdout.splitlines():
            parts = line.rsplit(":", 2)

            if len(parts) != 3:
                continue

            ssid, signal_text, security = parts

            ssid = ssid.strip()

            if not ssid:
                continue

            try:
                signal = int(signal_text)
            except ValueError:
                continue

            existing = networks.get(ssid)

            if existing is None or signal > existing["signal"]:
                networks[ssid] = {
                    "ssid": ssid,
                    "signal": signal,
                    "security": security.strip(),
                }

        return sorted(
            networks.values(),
            key=lambda network: network["signal"],
            reverse=True,
        )