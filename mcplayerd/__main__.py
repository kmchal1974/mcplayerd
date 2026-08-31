"""Command-line entry point for McPlayerD."""

from mcplayerd.daemon import run


def main() -> None:
    """Run McPlayerD."""
    run()


if __name__ == "__main__":
    main()