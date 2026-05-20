"""
Repository utilities - Handle repository resolution and validation
"""

import re
from typing import Optional

from ..config import REPOSITORIES, DEFAULT_REPO


class RepositoryError(Exception):
    """Raised when repository is invalid"""

    pass


def resolve_repository(repo_input: Optional[str] = None) -> str:
    """
    Resolve repository alias or owner/repo format

    Args:
        repo_input: Repository alias or owner/repo format (optional)

    Returns:
        Repository in owner/repo format

    Raises:
        RepositoryError: If repository is invalid

    Examples:
        >>> resolve_repository('symfony')
        'symfony/symfony'
        >>> resolve_repository('facebook/react')
        'facebook/react'
        >>> resolve_repository()
        'symfony/symfony'  # default
    """
    # Use default if not specified
    if not repo_input:
        return REPOSITORIES.get(DEFAULT_REPO, "symfony/symfony")

    # Check if it's an alias
    if repo_input in REPOSITORIES:
        return REPOSITORIES[repo_input]

    # Check if it's in owner/repo format
    if re.match(r"^[\w-]+/[\w-]+$", repo_input):
        return repo_input

    # Invalid format
    available = ", ".join(REPOSITORIES.keys())
    raise RepositoryError(
        f"Invalid repository: {repo_input}\n"
        f"Available aliases: {available}\n"
        f"Or use format: owner/repo"
    )


def get_repository_list() -> dict:
    """
    Get all configured repositories

    Returns:
        Dictionary of alias -> owner/repo
    """
    return REPOSITORIES.copy()


def get_default_repository() -> str:
    """
    Get the default repository

    Returns:
        Repository in owner/repo format
    """
    return REPOSITORIES.get(DEFAULT_REPO, "symfony/symfony")
