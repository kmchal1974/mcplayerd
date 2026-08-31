"""Core McPlayerD daemon application."""

from mcplayerd import __version__


def run() -> None:
    """Start McPlayerD."""
    print("McPlayerD starting")
    print(f"McPlayerD version {__version__}")