"""Read-only NetworkManager support for McPlayerD."""

import os
import shutil
import subprocess


class NetworkManagerStatus:
    """Read basic NetworkManager availability."""

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