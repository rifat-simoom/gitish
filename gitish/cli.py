"""
CLI Entry Point - Command-line interface
"""

import argparse
import sys

from .commands import AvailableIssuesCommand, ListReposCommand, ShowIssueCommand
from .config import APP_NAME, VERSION


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog="gitish",
        description="Find truly available GitHub issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list
  %(prog)s available symfony
  %(prog)s available laravel --label=bug --limit=10
  %(prog)s show 12345 symfony

Environment:
  GITHUB_TOKEN    GitHub personal access token (increases rate limit)
                  Get one at: https://github.com/settings/tokens
        """,
    )

    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list command
    subparsers.add_parser("list", help="List configured repositories")

    # available command
    available_parser = subparsers.add_parser(
        "available", help="Find available issues without linked PRs"
    )
    available_parser.add_argument("repo", nargs="?", help="Repository alias or owner/repo")
    available_parser.add_argument("--label", help="Filter by label")
    available_parser.add_argument(
        "--limit", type=int, default=20, help="Number of results to show (default: 20)"
    )

    # show command
    show_parser = subparsers.add_parser("show", help="Show detailed issue information")
    show_parser.add_argument("number", type=int, help="Issue number")
    show_parser.add_argument("repo", nargs="?", help="Repository alias or owner/repo")

    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Route to appropriate command
    try:
        if args.command == "list":
            command = ListReposCommand()
            sys.exit(command.execute())

        elif args.command == "available":
            command = AvailableIssuesCommand(repo=args.repo, label=args.label, limit=args.limit)
            sys.exit(command.execute())

        elif args.command == "show":
            command = ShowIssueCommand(number=args.number, repo=args.repo)
            sys.exit(command.execute())

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"❌ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
