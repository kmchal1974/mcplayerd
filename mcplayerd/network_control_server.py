from __future__ import annotations

import json
import os
import socket
from pathlib import Path

from mcplayerd.network_controller import NetworkController


CONTROL_SOCKET = Path("/run/mcplayer/network-control.sock")


class NetworkControlServer:
    """Local command interface for user-directed network control."""

    def __init__(
        self,
        controller: NetworkController | None = None,
        socket_path: Path = CONTROL_SOCKET,
    ) -> None:
        self.controller = controller or NetworkController()
        self.socket_path = socket_path

    def _handle_command(self, request: dict) -> dict:
        action = request.get("action")

        if action == "force_ap":
            success = self.controller.force_ap_mode()
        elif action == "automatic":
            success = self.controller.return_to_automatic()
        elif action == "list_saved":
            return {
                "ok": True,
                "action": action,
                "networks": self.controller.get_saved_networks(),
            }
        elif action == "scan_wifi":
            return {
                "ok": True,
                "action": action,
                "networks": self.controller.network_manager.scan_wifi_networks(),
            }
        elif action == "connect_saved":
            connection_name = request.get("connection", "")
            success = self.controller.connect_saved_network(
                connection_name
            )
        elif action == "add_network":
            ssid = str(request.get("ssid", "")).strip()
            password = str(request.get("password", ""))

            if not ssid:
                return {
                    "ok": False,
                    "error": "Missing SSID",
                }

            success = self.controller.add_and_connect_network(
                ssid,
                password,
            )
        elif action == "enable_autoconnect":
            connection_name = str(
                request.get("connection", "")
            ).strip()

            if not connection_name:
                return {
                    "ok": False,
                    "error": "Missing connection",
                }

            success = self.controller.enable_autoconnect(
                connection_name
            )
        elif action == "forget_network":
            connection_name = str(
                request.get("connection", "")
            ).strip()

            if not connection_name:
                return {
                    "ok": False,
                    "error": "Missing connection",
                }

            success = self.controller.forget_network(
                connection_name
            )
        elif action == "disable_autoconnect":
            connection_name = str(
                request.get("connection", "")
            ).strip()

            if not connection_name:
                return {
                    "ok": False,
                    "error": "Missing connection",
                }

            success = self.controller.disable_autoconnect(
                connection_name
            )
        else:
            return {
                "ok": False,
                "error": "Unknown action",
            }

        return {
            "ok": success,
            "action": action,
        }

    def serve_forever(self) -> None:
        """Listen for local dashboard network-control commands."""

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
                f"Network control socket ready: {self.socket_path}",
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
                            "Network control client disconnected before response",
                            flush=True,
                        )
                    except ConnectionResetError:
                        print(
                            "Network control client reset connection before response",
                            flush=True,
                        )