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

        if action not in ("play", "pause", "previous", "next", "stop"):
            return {
                "ok": False,
                "error": "Unknown action",
            }

        mpd = McPlayerMPDClient()

        try:
            mpd.connect()

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