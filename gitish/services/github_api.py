"""
GitHub API Service - Handles all GitHub API interactions
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from ..config import CACHE_DIR, CACHE_TTL, GITHUB_API_BASE, USER_AGENT


class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors"""

    pass


class RateLimitError(GitHubAPIError):
    """Raised when rate limit is exceeded"""

    pass


class GitHubAPI:
    """
    GitHub API client with caching and rate limit handling

    Provides methods to interact with GitHub's REST API including:
    - Fetching issues
    - Getting issue details, comments, and timeline
    - Detecting linked pull requests
    """

    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub API client

        Args:
            token: GitHub personal access token (optional)
        """
        self.base_url = GITHUB_API_BASE
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": USER_AGENT}

        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

        # Ensure cache directory exists
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _cache_key(self, url: str) -> Path:
        """Generate cache file path for URL"""
        import hashlib

        key = hashlib.md5(url.encode()).hexdigest()
        return CACHE_DIR / f"{key}.json"

    def _is_cache_valid(self, cache_file: Path) -> bool:
        """Check if cache file is still valid"""
        if not cache_file.exists():
            return False

        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        return datetime.now() - mtime < timedelta(seconds=CACHE_TTL)

    def _request(self, url: str, use_cache: bool = True) -> Dict:
        """
        Make HTTP request with caching

        Args:
            url: Full URL to request
            use_cache: Whether to use cached response

        Returns:
            Parsed JSON response

        Raises:
            RateLimitError: When rate limit is exceeded
            GitHubAPIError: For other API errors
        """
        cache_file = self._cache_key(url)

        # Check cache
        if use_cache and self._is_cache_valid(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)

        # Make request
        try:
            req = Request(url, headers=self.headers)
            with urlopen(req) as response:
                data = json.loads(response.read().decode())

                # Save to cache
                with open(cache_file, "w") as f:
                    json.dump(data, f)

                return data

        except HTTPError as e:
            if e.code == 403:
                raise RateLimitError(
                    "GitHub API rate limit exceeded. "
                    "Add GITHUB_TOKEN environment variable to increase limit. "
                    "Get token at: https://github.com/settings/tokens"
                )
            raise GitHubAPIError(f"GitHub API error: {e.code} - {e.reason}")

    def get_issues(self, repo: str, params: Optional[Dict] = None) -> List[Dict]:
        """
        Get issues for a repository

        Args:
            repo: Repository in owner/repo format
            params: Query parameters (state, labels, per_page, etc.)

        Returns:
            List of issue dictionaries
        """
        params = params or {}
        query_params = urlencode(params)
        url = f"{self.base_url}/repos/{repo}/issues?{query_params}"
        return self._request(url)

    def get_issue(self, repo: str, number: int) -> Dict:
        """
        Get a single issue

        Args:
            repo: Repository in owner/repo format
            number: Issue number

        Returns:
            Issue dictionary
        """
        url = f"{self.base_url}/repos/{repo}/issues/{number}"
        return self._request(url)

    def get_comments(self, repo: str, number: int) -> List[Dict]:
        """
        Get comments for an issue

        Args:
            repo: Repository in owner/repo format
            number: Issue number

        Returns:
            List of comment dictionaries
        """
        url = f"{self.base_url}/repos/{repo}/issues/{number}/comments"
        return self._request(url)

    def get_timeline(self, repo: str, number: int) -> List[Dict]:
        """
        Get timeline events for an issue

        Args:
            repo: Repository in owner/repo format
            number: Issue number

        Returns:
            List of timeline event dictionaries
        """
        url = f"{self.base_url}/repos/{repo}/issues/{number}/timeline"
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.mockingbird-preview+json"

        try:
            req = Request(url, headers=headers)
            with urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception:
            return []

    def get_linked_prs(self, repo: str, number: int) -> List[Dict]:
        """
        Get linked pull requests for an issue

        Checks the timeline for cross-referenced PRs

        Args:
            repo: Repository in owner/repo format
            number: Issue number

        Returns:
            List of linked PR dictionaries with keys:
            - number: PR number
            - title: PR title
            - state: open/closed
            - url: PR URL
            - user: PR author username
        """
        timeline = self.get_timeline(repo, number)
        linked_prs = []

        for event in timeline:
            if event.get("event") == "cross-referenced":
                source = event.get("source", {})
                if "issue" in source and "pull_request" in source["issue"]:
                    pr = source["issue"]
                    linked_prs.append(
                        {
                            "number": pr["number"],
                            "title": pr["title"],
                            "state": pr["state"],
                            "url": pr["html_url"],
                            "user": pr["user"]["login"],
                        }
                    )

        return linked_prs

    def has_linked_prs(self, repo: str, number: int) -> bool:
        """
        Check if an issue has any linked pull requests

        Args:
            repo: Repository in owner/repo format
            number: Issue number

        Returns:
            True if issue has linked PRs, False otherwise
        """
        return len(self.get_linked_prs(repo, number)) > 0
