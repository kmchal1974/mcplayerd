from __future__ import annotations

import json
import os
import socket
from pathlib import Path

from mcplayerd.mpd_client import McPlayerMPDClient


CONTROL_SOCKET = Path("/run/mcplayer/player-control.sock")


class PlayerControlServer:
    """Local command interface for MPD player control."""

    def __init__(
        self,
        socket_path: Path = CONTROL_SOCKET,
    ) -> None:
        self.socket_path = socket_path

    def _handle_command(self, request: dict) -> dict:
        """Execute one player-control command."""
        action = request.get("action")

        if action not in (
            "play",
            "pause",
            "previous",
            "next",
            "stop",
            "toggle",
            "volume",
            "seek",
            "shuffle",
            "repeat",
            "clear",
            "playindex",
            "remove_index",
            "move_index",
            "list_artists",
            "list_albums",
            "list_tracks",
            "list_saved_playlists",
            "load_saved_playlist",
            "add_track",
            "add_album",
            "play_track",
            "play_album",
        ):
            return {
                "ok": False,
                "error": "Unknown action",
            }

        mpd = McPlayerMPDClient()

        try:
            mpd.connect()

            if action == "list_saved_playlists":
                return {
                    "ok": True,
                    "action": action,
                    "playlists": mpd.list_saved_playlists(),
                }
            if action == "list_artists":
                return {
                    "ok": True,
                    "action": action,
                    "artists": mpd.list_album_artists(),
                }
            if action == "list_albums":
                album_artist = str(request.get("artist", ""))
                return {
                    "ok": True,
                    "action": action,
                    "artist": album_artist,
                    "albums": mpd.list_albums(album_artist),
                }
            if action == "list_tracks":
                album_artist = str(request.get("artist", ""))
                album = str(request.get("album", ""))
                return {
                    "ok": True,
                    "action": action,
                    "artist": album_artist,
                    "album": album,
                    "tracks": mpd.list_album_tracks(
                        album_artist,
                        album,
                    ),
                }
            if action == "play":
                mpd.play()
            elif action == "pause":
                mpd.pause()
            elif action == "previous":
                mpd.previous()
            elif action == "next":
                mpd.next()
            elif action == "stop":
                mpd.stop()
            elif action == "toggle":
                mpd.toggle()
            elif action == "volume":
                volume = max(0, min(100, int(request.get("value", 0))))
                mpd.set_volume(volume)
            elif action == "seek":
                seconds = max(0, int(request.get("value", 0)))
                mpd.seek(seconds)
            elif action == "shuffle":
                value = request.get("value")
                if value is None:
                    mpd.toggle_random()
                else:
                    mpd.set_random(bool(value))
            elif action == "repeat":
                value = request.get("value")
                if value is None:
                    mpd.toggle_repeat()
                else:
                    mpd.set_repeat(bool(value))
            elif action == "clear":
                mpd.clear()
            elif action == "playindex":
                track = max(1, int(request.get("value", 1)))
                mpd.play_index(track)
            elif action == "remove_index":
                track = max(1, int(request.get("value", 1)))
                mpd.remove_index(track)
            elif action == "move_index":
                track = max(1, int(request.get("track", 1)))
                destination = max(1, int(request.get("destination", 1)))
                mpd.move_index(track, destination)
            elif action == "load_saved_playlist":
                name = str(request.get("name", ""))
                mpd.load_saved_playlist(name)
            elif action == "add_track":
                file = str(request.get("file", ""))
                mpd.add_track(file)
            elif action == "play_track":
                file = str(request.get("file", ""))
                mpd.play_track(file)
            elif action == "add_album":
                album_artist = str(request.get("artist", ""))
                album = str(request.get("album", ""))
                mpd.add_album(
                    album_artist,
                    album,
                )
            elif action == "play_album":
                album_artist = str(request.get("artist", ""))
                album = str(request.get("album", ""))
                mpd.play_album(
                    album_artist,
                    album,
                )

            status = mpd.get_status()

            return {
                "ok": True,
                "action": action,
                "playback": {
                    "state": status.get("state", "unknown"),
                    "volume": (
                        int(status["volume"])
                        if "volume" in status
                        else None
                    ),
                },
            }
        finally:
            try:
                mpd.disconnect()
            except Exception:
                pass

    def serve_forever(self) -> None:
        """Listen for local dashboard player-control commands."""
        self.socket_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if self.socket_path.exists():
            self.socket_path.unlink()

        with socket.socket(
            socket.AF_UNIX,
            socket.SOCK_STREAM,
        ) as server:
            server.bind(str(self.socket_path))

            os.chmod(
                self.socket_path,
                0o660,
            )

            server.listen()

            print(
                f"Player control socket ready: {self.socket_path}",
                flush=True,
            )

            while True:
                connection, _ = server.accept()

                with connection:
                    try:
                        raw_request = connection.recv(4096)

                        request = json.loads(
                            raw_request.decode("utf-8")
                        )

                        response = self._handle_command(
                            request
                        )

                    except Exception as exc:
                        response = {
                            "ok": False,
                            "error": str(exc),
                        }

                    try:
                        connection.sendall(
                            json.dumps(response).encode("utf-8")
                        )
                    except BrokenPipeError:
                        print(
                            "Player control client disconnected before response",
                            flush=True,
                        )
                    except ConnectionResetError:
                        print(
                            "Player control client reset connection before response",
                            flush=True,
                        )