"""
Formatting utilities - Beautiful console output
"""

from typing import List, Dict, Any


def truncate_text(text: str, max_length: int = 60) -> str:
    """
    Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def format_table(headers: List[str], rows: List[List[str]], widths: List[int]) -> str:
    """
    Format data as a table
    
    Args:
        headers: Column headers
        rows: Data rows
        widths: Column widths
        
    Returns:
        Formatted table string
    """
    lines = []
    
    # Header
    header_line = "  " + "  ".join(
        h.ljust(w) for h, w in zip(headers, widths)
    )
    lines.append(header_line)
    
    # Separator
    separator = "  " + "  ".join("-" * w for w in widths)
    lines.append(separator)
    
    # Rows
    for row in rows:
        row_line = "  " + "  ".join(
            str(cell).ljust(w) for cell, w in zip(row, widths)
        )
        lines.append(row_line)
    
    return "\n".join(lines)


def format_issue(issue: Dict[str, Any], show_labels: bool = True) -> str:
    """
    Format issue for display
    
    Args:
        issue: Issue dictionary
        show_labels: Whether to show labels
        
    Returns:
        Formatted issue string
    """
    lines = []
    
    # Title and number
    lines.append(f"  #{issue['number']:<6} {truncate_text(issue['title'], 60)}")
    
    # Labels
    if show_labels and issue.get('labels'):
        label_names = [l['name'] for l in issue['labels'][:3]]
        labels_str = ', '.join(label_names)
        if len(issue['labels']) > 3:
            labels_str += f" +{len(issue['labels']) - 3}"
        lines.append(f"         Labels: {labels_str}")
    
    # Metadata
    updated = issue['updated_at'][:10]
    lines.append(f"         Comments: {issue['comments']}  Updated: {updated}")
    
    return "\n".join(lines)


def format_pr_list(prs: List[Dict[str, Any]]) -> str:
    """
    Format list of pull requests
    
    Args:
        prs: List of PR dictionaries
        
    Returns:
        Formatted PR list string
    """
    if not prs:
        return "No linked pull requests"
    
    lines = []
    for pr in prs:
        state_icon = '○' if pr['state'] == 'open' else '●'
        state_text = pr['state'].title()
        lines.append(f"  {state_icon} {state_text} PR #{pr['number']}: {pr['title']}")
        lines.append(f"    by {pr['user']} - {pr['url']}")
    
    return "\n".join(lines)


def format_labels(labels: List[Dict[str, Any]], max_display: int = 3) -> str:
    """
    Format labels for display
    
    Args:
        labels: List of label dictionaries
        max_display: Maximum number of labels to show
        
    Returns:
        Formatted labels string
    """
    if not labels:
        return "None"
    
    label_names = [l['name'] for l in labels[:max_display]]
    result = ', '.join(label_names)
    
    if len(labels) > max_display:
        result += f" +{len(labels) - max_display}"
    
    return result
