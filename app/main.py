"""Technical entry point for the application bootstrap."""

from app.bootstrap import bootstrap_application


def main() -> int:
    """Initialize the technical base without running business workflows."""
    result = bootstrap_application()
    print(result.status_message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
