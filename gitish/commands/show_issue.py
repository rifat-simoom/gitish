"""
Show Issue Command - Display detailed issue information
"""

import sys
from typing import Optional

from ..services import GitHubAPI, RateLimitError, GitHubAPIError
from ..utils import resolve_repository, RepositoryError, format_pr_list, format_labels


class ShowIssueCommand:
    """Command to show detailed issue information"""

    def __init__(self, number: int, repo: Optional[str] = None):
        """
        Initialize command

        Args:
            number: Issue number
            repo: Repository alias or owner/repo
        """
        self.number = number
        self.repo_input = repo
        self.api = GitHubAPI()

    def execute(self) -> int:
        """
        Execute the show issue command

        Returns:
            Exit code (0 for success, 1 for error)
        """
        try:
            # Resolve repository
            repo = resolve_repository(self.repo_input)

            print(f"\n🔍 Fetching issue #{self.number} from {repo}...\n")

            # Fetch issue data
            issue = self.api.get_issue(repo, self.number)
            comments = self.api.get_comments(repo, self.number)
            linked_prs = self.api.get_linked_prs(repo, self.number)

            # Display issue header
            print(f"Issue #{issue['number']}: {issue['title']}")
            print(f"State: {issue['state']}")
            print(f"Author: {issue['user']['login']}")
            print(f"Created: {issue['created_at'][:10]}")
            print(f"URL: {issue['html_url']}")

            # Labels
            if issue["labels"]:
                print(f"Labels: {format_labels(issue['labels'], max_display=10)}")

            # Linked PRs
            if linked_prs:
                print(f"\n=== Linked Pull Requests ({len(linked_prs)}) ===")
                print(format_pr_list(linked_prs))
                print(
                    f"\n⚠️  This issue has linked PRs. Check if someone is already working on it!"
                )

            # Description
            print(f"\n=== Description ===")
            print(issue["body"] or "No description provided.")

            # Comments
            if comments:
                print(f"\n=== Comments ({len(comments)}) ===")
                for i, comment in enumerate(comments, 1):
                    print(
                        f"\n--- Comment #{i} by {comment['user']['login']} on {comment['created_at'][:10]} ---"
                    )
                    body = comment["body"]
                    if len(body) > 500:
                        print(body[:500] + "\n... (truncated)")
                    else:
                        print(body)
            else:
                print(f"\n=== Comments ===")
                print("No comments yet.")

            # Next steps
            print(f"\n=== Next Steps ===")
            if linked_prs:
                print("1. Check linked PRs to see current progress")
                print("2. Consider helping with existing PR or wait for it to be merged")
            else:
                print("1. Read the full issue and comments")
                print("2. Comment to express interest")
                print("3. Fork the repository and create a branch")
                print("4. Implement the fix/feature with tests")
                print("5. Submit a pull request")
            print()

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
