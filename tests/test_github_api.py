"""
Tests for GitHub API client
"""

from unittest.mock import Mock, patch

import pytest

from gitish.services.github_api import GitHubAPI, RateLimitError


class TestGitHubAPI:
    """Test GitHub API client"""

    def test_init_without_token(self):
        """Test initialization without token"""
        api = GitHubAPI()
        assert api.token is None
        assert "Authorization" not in api.headers

    def test_init_with_token(self):
        """Test initialization with token"""
        api = GitHubAPI(token="test_token")
        assert api.token == "test_token"
        assert api.headers["Authorization"] == "Bearer test_token"

    def test_init_with_env_token(self, monkeypatch):
        """Test initialization with environment token"""
        monkeypatch.setenv("GITHUB_TOKEN", "env_token")
        api = GitHubAPI()
        assert api.token == "env_token"
        assert api.headers["Authorization"] == "Bearer env_token"

    @patch("gitish.services.github_api.urlopen")
    def test_request_success(self, mock_urlopen):
        """Test successful API request"""
        # Mock response
        mock_response = Mock()
        mock_response.read.return_value = b'{"test": "data"}'
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)
        mock_urlopen.return_value = mock_response

        api = GitHubAPI()
        result = api._request("https://api.github.com/test", use_cache=False)

        assert result == {"test": "data"}

    @patch("gitish.services.github_api.urlopen")
    def test_request_rate_limit(self, mock_urlopen):
        """Test rate limit error"""
        from urllib.error import HTTPError

        mock_urlopen.side_effect = HTTPError(
            "https://api.github.com/test", 403, "Forbidden", {}, None
        )

        api = GitHubAPI()
        with pytest.raises(RateLimitError):
            api._request("https://api.github.com/test", use_cache=False)

    def test_get_issues(self):
        """Test getting issues"""
        api = GitHubAPI()
        with patch.object(api, "_request", return_value=[{"number": 1}]):
            issues = api.get_issues("test/repo", {"state": "open"})
            assert len(issues) == 1
            assert issues[0]["number"] == 1

    def test_get_issue(self):
        """Test getting single issue"""
        api = GitHubAPI()
        with patch.object(api, "_request", return_value={"number": 123}):
            issue = api.get_issue("test/repo", 123)
            assert issue["number"] == 123

    def test_get_linked_prs(self):
        """Test getting linked PRs"""
        api = GitHubAPI()

        # Mock timeline with cross-referenced PR
        timeline = [
            {
                "event": "cross-referenced",
                "source": {
                    "issue": {
                        "number": 456,
                        "title": "Test PR",
                        "state": "open",
                        "html_url": "https://github.com/test/repo/pull/456",
                        "user": {"login": "testuser"},
                        "pull_request": {},
                    }
                },
            }
        ]

        with patch.object(api, "get_timeline", return_value=timeline):
            prs = api.get_linked_prs("test/repo", 123)
            assert len(prs) == 1
            assert prs[0]["number"] == 456
            assert prs[0]["title"] == "Test PR"

    def test_has_linked_prs(self):
        """Test checking if issue has linked PRs"""
        api = GitHubAPI()

        with patch.object(api, "get_linked_prs", return_value=[{"number": 1}]):
            assert api.has_linked_prs("test/repo", 123) is True

        with patch.object(api, "get_linked_prs", return_value=[]):
            assert api.has_linked_prs("test/repo", 123) is False
