"""
Pytest configuration and fixtures
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_cache_dir(monkeypatch):
    """Create a temporary cache directory for tests"""
    temp_dir = Path(tempfile.mkdtemp())

    # Patch the cache directory
    from gitish import config

    monkeypatch.setattr(config, "CACHE_DIR", temp_dir / "cache")

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_github_response():
    """Mock GitHub API response"""
    return {
        "number": 123,
        "title": "Test Issue",
        "state": "open",
        "labels": [{"name": "bug"}, {"name": "help wanted"}],
        "comments": 5,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-15T00:00:00Z",
        "html_url": "https://github.com/test/repo/issues/123",
        "user": {"login": "testuser"},
        "body": "Test issue description",
    }


@pytest.fixture
def mock_issues_list():
    """Mock list of issues"""
    return [
        {
            "number": 1,
            "title": "Issue 1",
            "state": "open",
            "labels": [{"name": "bug"}],
            "comments": 0,
            "updated_at": "2024-01-01T00:00:00Z",
        },
        {
            "number": 2,
            "title": "Issue 2",
            "state": "open",
            "labels": [{"name": "feature"}],
            "comments": 3,
            "updated_at": "2024-01-02T00:00:00Z",
        },
    ]
