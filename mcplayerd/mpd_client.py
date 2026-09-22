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

    def play(self) -> None:
        """Start or resume MPD playback."""
        self.client.play()

    def pause(self) -> None:
        """Pause MPD playback."""
        self.client.pause(1)

    def previous(self) -> None:
        """Skip to the previous MPD track."""
        self.client.previous()

    def next(self) -> None:
        """Skip to the next MPD track."""
        self.client.next()

    def stop(self) -> None:
        """Stop MPD playback."""
        self.client.stop()

    def toggle(self) -> None:
        """Toggle MPD between play and pause."""
        status = self.client.status()

        if status.get("state") == "play":
            self.client.pause(1)
        else:
            self.client.play()

    def set_volume(self, volume: int) -> None:
        """Set MPD volume from 0 to 100."""
        volume = max(0, min(100, volume))
        self.client.setvol(volume)

    def seek(self, seconds: int) -> None:
        """Seek to an absolute position in the current track."""
        seconds = max(0, seconds)
        self.client.seekcur(seconds)
