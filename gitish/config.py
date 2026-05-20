"""
Configuration for GitHub Issue Finder
"""

from pathlib import Path
from typing import Dict

# Application settings
VERSION = "1.0.0"
APP_NAME = "GitHub Issue Finder"
USER_AGENT = f"{APP_NAME}/{VERSION}"

# Cache settings
CACHE_DIR = Path.home() / ".gitish" / "cache"
CACHE_TTL = 300  # 5 minutes

# GitHub API
GITHUB_API_BASE = "https://api.github.com"

# Default repository
DEFAULT_REPO = "symfony"

# Pre-configured repositories
REPOSITORIES: Dict[str, str] = {
    # PHP
    "symfony": "symfony/symfony",
    "laravel": "laravel/framework",
    "phpunit": "phpunit/phpunit",
    "doctrine": "doctrine/orm",
    "guzzle": "guzzle/guzzle",
    # JavaScript
    "react": "facebook/react",
    "vue": "vuejs/core",
    "angular": "angular/angular",
    "node": "nodejs/node",
    "typescript": "microsoft/TypeScript",
    # Python
    "django": "django/django",
    "flask": "pallets/flask",
    "pytest": "pytest-dev/pytest",
    # Other
    "rust": "rust-lang/rust",
    "go": "golang/go",
    "rails": "rails/rails",
    "dotnet": "dotnet/runtime",
}
