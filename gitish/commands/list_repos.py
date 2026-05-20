"""
List Repositories Command
"""

from ..config import DEFAULT_REPO
from ..utils import get_repository_list


class ListReposCommand:
    """Command to list all configured repositories"""
    
    def execute(self) -> int:
        """
        Execute the list repositories command
        
        Returns:
            Exit code (0 for success)
        """
        repos = get_repository_list()
        
        if not repos:
            print("⚠️  No repositories configured.")
            return 0
        
        print("\n📋 Configured Repositories:\n")
        
        # Calculate max alias length for alignment
        max_alias_len = max(len(alias) for alias in repos.keys())
        
        for alias, full_name in repos.items():
            default_marker = '✓' if alias == DEFAULT_REPO else ' '
            print(f"  {default_marker} {alias:<{max_alias_len}}  {full_name}")
        
        print("\n💡 Usage:")
        print("   gitish available <repo>")
        print("   gitish show <number> <repo>")
        print()
        
        return 0
