"""
Tests for repository utilities
"""

import pytest
from gitish.utils.repository import resolve_repository, get_repository_list, RepositoryError


class TestRepositoryUtils:
    """Test repository utility functions"""

    def test_resolve_repository_alias(self):
        """Test resolving repository alias"""
        result = resolve_repository("symfony")
        assert result == "symfony/symfony"

    def test_resolve_repository_owner_repo(self):
        """Test resolving owner/repo format"""
        result = resolve_repository("facebook/react")
        assert result == "facebook/react"

    def test_resolve_repository_default(self):
        """Test resolving default repository"""
        result = resolve_repository(None)
        assert result == "symfony/symfony"

    def test_resolve_repository_invalid(self):
        """Test resolving invalid repository"""
        with pytest.raises(RepositoryError):
            resolve_repository("invalid-format")

    def test_get_repository_list(self):
        """Test getting repository list"""
        repos = get_repository_list()
        assert isinstance(repos, dict)
        assert "symfony" in repos
        assert "laravel" in repos
        assert repos["symfony"] == "symfony/symfony"
