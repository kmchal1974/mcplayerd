from __future__ import annotations

from mcplayerd.network_manager import NetworkManagerStatus


class NetworkController:
    """User-directed McPlayer network control."""

    def __init__(
        self,
        network_manager: NetworkManagerStatus | None = None,
        hotspot_connection: str = "McPlayer-AP",
    ) -> None:
        self.network_manager = network_manager or NetworkManagerStatus()
        self.hotspot_connection = hotspot_connection

    def force_ap_mode(self) -> bool:
        """Start McPlayer AP mode and leave it active."""
        return self.network_manager.start_fallback_ap(
            self.hotspot_connection
        )

    def connect_saved_network(self, connection_name: str) -> bool:
        """Connect to a specific saved Wi-Fi connection."""
        connection_name = connection_name.strip()

        if not connection_name:
            return False

        if connection_name == self.hotspot_connection:
            return self.force_ap_mode()

        known_connections = (
            self.network_manager.get_known_wifi_connections()
        )

        if connection_name not in known_connections:
            return False

        return self.network_manager.activate_wifi_connection(
            connection_name
        )

    def add_and_connect_network(
        self,
        ssid: str,
        password: str = "",
    ) -> bool:
        ssid = ssid.strip()

        if not ssid:
            return False

        return self.network_manager.add_wifi_connection(
            ssid,
            password,
        )

    def return_to_automatic(self) -> bool:
        """Keep usable Wi-Fi, otherwise try saved Wi-Fi once, then use AP."""
        if self.network_manager.has_usable_wifi(
            self.hotspot_connection
        ):
            return True

        recovered_connection = (
            self.network_manager.try_saved_wifi_connections(
                self.hotspot_connection
            )
        )

        if recovered_connection is not None:
            return True

        return self.force_ap_mode()

    def get_saved_networks(self) -> list[dict]:
        """Return saved normal Wi-Fi connections with current signal."""

        saved_connections = [
            name
            for name in self.network_manager.get_known_wifi_connections()
            if name != self.hotspot_connection
        ]

        signal_results = (
            self.network_manager.get_known_wifi_signals()
        )

        signal_by_connection = {
            item["connection"]: item
            for item in signal_results
        }

        networks = []

        for connection_name in saved_connections:
            signal_info = signal_by_connection.get(
                connection_name
            )

            if signal_info is None:
                networks.append({
                    "name": connection_name,
                    "ssid": connection_name,
                    "signal": None,
                })
            else:
                networks.append({
                    "name": connection_name,
                    "ssid": signal_info["ssid"],
                    "signal": signal_info["signal"],
                })

        return networks

    def enable_autoconnect(
        self,
        connection_name: str,
    ) -> bool:
        connection_name = connection_name.strip()

        if not connection_name:
            return False

        if connection_name == self.hotspot_connection:
            return False

        return self.network_manager.set_connection_autoconnect(
            connection_name,
            True,
        )

    def disable_autoconnect(
        self,
        connection_name: str,
    ) -> bool:
        connection_name = connection_name.strip()

        if not connection_name:
            return False

        if connection_name == self.hotspot_connection:
            return False

        return self.network_manager.set_connection_autoconnect(
            connection_name,
            False,
        )