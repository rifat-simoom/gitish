"""
Available Issues Command - Find issues without linked PRs
"""

import sys
from typing import Optional

from ..services import GitHubAPI, RateLimitError, GitHubAPIError
from ..utils import resolve_repository, RepositoryError, format_issue


class AvailableIssuesCommand:
    """Command to find available issues without linked PRs"""

    def __init__(self, repo: Optional[str] = None, label: Optional[str] = None, limit: int = 20):
        """
        Initialize command

        Args:
            repo: Repository alias or owner/repo
            label: Filter by label
            limit: Maximum number of results
        """
        self.repo_input = repo
        self.label = label
        self.limit = limit
        self.api = GitHubAPI()

    def execute(self) -> int:
        """
        Execute the available issues command

        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Resolve repository
            repo = resolve_repository(self.repo_input)

            print(f"\n🔍 Fetching issues from {repo}...")

            # Build query parameters
            params = {
                "state": "open",
                "per_page": 100,
            }

            if self.label:
                params["labels"] = self.label
                print(f"   Filtering by label: {self.label}")

            # Fetch issues
            issues = self.api.get_issues(repo, params)

            # Filter out pull requests and issues with linked PRs
            available = []
            for issue in issues:
                # Skip if it's a PR itself
                if "pull_request" in issue:
                    continue

                # Check for linked PRs
                linked_prs = self.api.get_linked_prs(repo, issue["number"])
                if not linked_prs:
                    available.append(issue)

            # Display results
            if not available:
                print("\n⚠️  No issues found. Try different filters or repository.\n")
                return 0

            print(f"\nFound {len(available)} issues without linked PRs\n")

            # Show as table
            self._display_table(available[: self.limit], repo)

            if len(available) > self.limit:
                print(
                    f"\nShowing {self.limit} of {len(available)} issues. Use --limit to see more.\n"
                )

            return 0

        except RepositoryError as e:
            print(f"❌ {e}", file=sys.stderr)
            return 1
        except RateLimitError as e:
            print(f"⚠️  {e}", file=sys.stderr)
            return 1
        except GitHubAPIError as e:
            print(f"❌ {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"❌ Unexpected error: {e}", file=sys.stderr)
            return 1

    def _display_table(self, issues, repo):
        """Display issues in a beautiful table format"""
        if not issues:
            return

        # Table header
        print(
            "+" + "-" * 8 + "+" + "-" * 57 + "+" + "-" * 42 + "+" + "-" * 10 + "+" + "-" * 12 + "+"
        )
        print(f"| {'#':<6} | {'Title':<55} | {'Labels':<40} | {'Comments':<8} | {'Updated':<10} |")
        print(
            "+" + "-" * 8 + "+" + "-" * 57 + "+" + "-" * 42 + "+" + "-" * 10 + "+" + "-" * 12 + "+"
        )

        # Table rows
        for issue in issues:
            # Prepare data
            number = str(issue["number"])
            title = self._truncate(issue["title"], 55)

            # Format labels
            if issue.get("labels"):
                label_names = [l["name"] for l in issue["labels"][:3]]
                labels = ", ".join(label_names)
                if len(issue["labels"]) > 3:
                    labels += f"... +{len(issue['labels']) - 3}"
                labels = self._truncate(labels, 40)
            else:
                labels = ""

            comments = str(issue["comments"])
            updated = issue["updated_at"][:10]

            # Print row
            print(f"| {number:<6} | {title:<55} | {labels:<40} | {comments:<8} | {updated:<10} |")

        # Table footer
        print(
            "+" + "-" * 8 + "+" + "-" * 57 + "+" + "-" * 42 + "+" + "-" * 10 + "+" + "-" * 12 + "+"
        )

        # Tips
        print("\n💡")
        print(f"   • Use: gitish show <number> --repo=alias")
        print(f'   • Use: --label="Feature" to filter by label')
        print(f'   • Use: --label="Bug" to find bugs')
        print(f'   • Use: --label="DX" for Developer Experience issues')
        print(f"   • Use: --limit=50 to see more results")

    def _truncate(self, text, max_length):
        """Truncate text to fit in table cell"""
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."
