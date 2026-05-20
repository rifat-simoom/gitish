"""
Tests for formatting utilities
"""

from gitish.utils.formatters import format_labels, format_pr_list, truncate_text


class TestFormatters:
    """Test formatting utilities"""

    def test_truncate_text_short(self):
        """Test truncating short text"""
        result = truncate_text("Short text", 20)
        assert result == "Short text"

    def test_truncate_text_long(self):
        """Test truncating long text"""
        result = truncate_text("This is a very long text that needs truncation", 20)
        assert len(result) == 20
        assert result.endswith("...")

    def test_format_labels_empty(self):
        """Test formatting empty labels"""
        result = format_labels([])
        assert result == "None"

    def test_format_labels_few(self):
        """Test formatting few labels"""
        labels = [{"name": "bug"}, {"name": "help wanted"}]
        result = format_labels(labels)
        assert result == "bug, help wanted"

    def test_format_labels_many(self):
        """Test formatting many labels"""
        labels = [
            {"name": "bug"},
            {"name": "help wanted"},
            {"name": "good first issue"},
            {"name": "documentation"},
        ]
        result = format_labels(labels, max_display=2)
        assert "bug, help wanted" in result
        assert "+2" in result

    def test_format_pr_list_empty(self):
        """Test formatting empty PR list"""
        result = format_pr_list([])
        assert result == "No linked pull requests"

    def test_format_pr_list_with_prs(self):
        """Test formatting PR list"""
        prs = [
            {
                "number": 123,
                "title": "Test PR",
                "state": "open",
                "url": "https://github.com/test/repo/pull/123",
                "user": "testuser",
            }
        ]
        result = format_pr_list(prs)
        assert "PR #123" in result
        assert "Test PR" in result
        assert "testuser" in result
