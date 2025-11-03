"""Entry point for the LLM Context Manager application"""

import argparse
from src.ui.app import ChatManagerApp


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="LLM Context Manager - Manage and compress chat histories"
    )
    parser.add_argument(
        "--db",
        default="sqlite:///data/chat_history.db",
        help="Database URL (default: sqlite:///data/chat_history.db)",
    )

    args = parser.parse_args()

    app = ChatManagerApp(db_url=args.db)
    app.run()


if __name__ == "__main__":
    main()
