"""MPD connection support for McPlayerD."""

from mpd import MPDClient


class McPlayerMPDClient:
    """Manage the connection between McPlayerD and MPD."""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6600,
        timeout: float = 5.0,
    ) -> None:
        self.host = host
        self.port = port
        self.client = MPDClient()
        self.client.timeout = timeout
        self.client.idletimeout = None

    def connect(self) -> None:
        """Connect to MPD."""
        self.client.connect(self.host, self.port)

    def disconnect(self) -> None:
        """Close the MPD connection cleanly."""
        try:
            self.client.close()
        finally:
            self.client.disconnect()

    def get_status(self) -> dict:
        """Return the current MPD playback status."""
        return self.client.status()

    def get_current_song(self) -> dict:
        """Return metadata for the current song."""
        return self.client.currentsong()

    def wait_for_change(self) -> list[str]:
        """Wait for an MPD player or playlist change."""
        return self.client.idle("player", "playlist")