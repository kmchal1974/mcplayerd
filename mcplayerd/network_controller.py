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
        password: str,
    ) -> bool:
        """Add a new Wi-Fi network and connect to it."""
        ssid = ssid.strip()

        if not ssid or not password:
            return False

        return self.network_manager.add_wifi_connection(
            ssid,
            password,
        )

    def return_to_automatic(self) -> bool:
        """Try saved Wi-Fi once; otherwise remain in AP mode."""
        recovered_connection = (
            self.network_manager.try_saved_wifi_connections(
                self.hotspot_connection
            )
        )

        if recovered_connection is not None:
            return True

        return self.force_ap_mode()