"""Content writing utilities for formatting and saving output."""
from pathlib import Path
from typing import Dict, Any, List
import json

def format_markdown_section(title: str, content: str) -> str:
    """Format content as a markdown section.
    
    Args:
        title: Section title
        content: Section content
        
    Returns:
        str: Formatted markdown section
    """
    return f"## {title}\n\n{content}\n\n"

def format_social_post(title: str, content: str, platform: str) -> str:
    """Format a social media post.
    
    Args:
        title: Post title (e.g., "Twitter Post 1")
        content: Post content
        platform: Platform name (twitter, linkedin, instagram)
        
    Returns:
        str: Formatted social media post
    """
    platform_icons = {
        'twitter': '🐦',
        'linkedin': '💼',
        'instagram': '📸'
    }
    
    icon = platform_icons.get(platform.lower(), '📱')
    return f"### {icon} {title}\n\n{content}\n\n"

def format_show_note(timestamp: str, title: str, content: str) -> str:
    """Format a show note entry.
    
    Args:
        timestamp: Timestamp in format MM:SS
        title: Section title
        content: Section content
        
    Returns:
        str: Formatted show note entry
    """
    return f"[{timestamp}] **{title}**\n{content}\n\n"

def save_content(content: str, filename: str, output_dir: Path) -> None:
    """Save content to a file.
    
    Args:
        content: Content to save
        filename: Output filename
        output_dir: Output directory path
    """
    output_path = output_dir / filename
    output_path.write_text(content, encoding='utf-8')
    print(f"Saved: {filename}")

def load_template(template_name: str) -> Dict[str, Any]:
    """Load a content template.
    
    Args:
        template_name: Name of template to load
        
    Returns:
        Dict[str, Any]: Template configuration
    """
    template_path = Path(__file__).parent / "templates" / f"{template_name}.json"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_name}")
        
    return json.loads(template_path.read_text())

def apply_template(content: str, template: Dict[str, Any]) -> str:
    """Apply a template to content.
    
    Args:
        content: Raw content
        template: Template configuration
        
    Returns:
        str: Formatted content
    """
    if template.get('format') == 'markdown':
        return format_markdown_section(template['title'], content)
    elif template.get('format') == 'social':
        return format_social_post(
            template['title'],
            content,
            template['platform']
        )
    elif template.get('format') == 'show_note':
        return format_show_note(
            template['timestamp'],
            template['title'],
            content
        )
    else:
        return content
