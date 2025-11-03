"""Text formatting utilities"""

from rich.text import Text


def format_message_label(message, max_length=40):
    """Format message for display in tree"""
    content = message.content[:max_length]
    if len(message.content) > max_length:
        content += "..."

    if message.speaker == "user":
        icon = "👤"
        style = "bold cyan"
    else:
        icon = "🤖"
        style = "bold green"

    timestamp_str = message.timestamp.strftime("%H:%M")

    label = Text()
    label.append(f"{icon} ", style="")
    label.append(f"[{timestamp_str}] ", style="dim")
    label.append(content, style=style)

    return label


def format_message_detail(message):
    """Format full message details"""
    print(f"DEBUG format_message_detail called for message {message.id}")  # DEBUG

    timestamp_str = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")

    if message.speaker == "user":
        border_style = "cyan"
        icon = "👤 User"
    else:
        border_style = "green"
        icon = "🤖 Assistant"

    content_text = Text()
    content_text.append(f"{icon}\n", style=f"bold {border_style}")
    content_text.append(f"{timestamp_str}\n", style="dim")
    content_text.append(
        f"Message ID: {message.id} | Parent: {message.parent_id or 'Root'}\n\n",
        style="dim italic",
    )
    content_text.append(message.content, style="white")

    print(f"DEBUG content_text length: {len(str(content_text))}")  # DEBUG
    print(f"DEBUG border_style: {border_style}")  # DEBUG

    return content_text, border_style
