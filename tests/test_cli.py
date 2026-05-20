"""
Tests for CLI interface
"""

from unittest.mock import Mock, patch

import pytest

from gitish.cli import create_parser, main


class TestCLI:
    """Test CLI interface"""

    def test_create_parser(self):
        """Test parser creation"""
        parser = create_parser()
        assert parser is not None
        assert parser.prog == "gitish"

    def test_parser_list_command(self):
        """Test list command parsing"""
        parser = create_parser()
        args = parser.parse_args(["list"])
        assert args.command == "list"

    def test_parser_available_command(self):
        """Test available command parsing"""
        parser = create_parser()
        args = parser.parse_args(["available", "symfony"])
        assert args.command == "available"
        assert args.repo == "symfony"

    def test_parser_available_with_label(self):
        """Test available command with label"""
        parser = create_parser()
        args = parser.parse_args(["available", "symfony", "--label=bug"])
        assert args.command == "available"
        assert args.repo == "symfony"
        assert args.label == "bug"

    def test_parser_show_command(self):
        """Test show command parsing"""
        parser = create_parser()
        args = parser.parse_args(["show", "123", "symfony"])
        assert args.command == "show"
        assert args.number == 123
        assert args.repo == "symfony"

    @patch("gitish.cli.ListReposCommand")
    def test_main_list_command(self, mock_command):
        """Test main with list command"""
        mock_instance = Mock()
        mock_instance.execute.return_value = 0
        mock_command.return_value = mock_instance

        with patch("sys.argv", ["gitish", "list"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    @patch("gitish.cli.AvailableIssuesCommand")
    def test_main_available_command(self, mock_command):
        """Test main with available command"""
        mock_instance = Mock()
        mock_instance.execute.return_value = 0
        mock_command.return_value = mock_instance

        with patch("sys.argv", ["gitish", "available", "symfony"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
