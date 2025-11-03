"""Graph/Flowchart visualization of conversation tree"""

from pathlib import Path
from textual.widgets import Static
from textual.containers import ScrollableContainer
from textual.binding import Binding
from rich.text import Text

from src.database.models import Message


class GraphView(ScrollableContainer):
    """ASCII flowchart view of conversation tree"""

    CSS_PATH = Path(__file__).with_suffix(".tcss")

    BINDINGS = [
        Binding("j", "scroll_down", "Down", show=False),
        Binding("k", "scroll_up", "Up", show=False),
        Binding("g", "scroll_home", "Top", show=False),
        Binding("G", "scroll_end", "Bottom", show=False),
        Binding("d", "page_down", "Page Down", show=False),
        Binding("u", "page_up", "Page Up", show=False),
        Binding("+", "zoom_in", "Zoom In", show=False),
        Binding("-", "zoom_out", "Zoom Out", show=False),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_message = None
        self.compact_mode = False

    def compose(self):
        yield Static("Loading graph view...", classes="graph-content")

    def show_graph(self, session, selected_message=None):
        """Display the conversation as a flowchart/graph"""
        self.current_message = selected_message

        root_messages = session.query(Message).filter_by(parent_id=None).all()
        graph_text = self._build_graph(root_messages, session)

        content = self.query_one(".graph-content", Static)
        content.update(graph_text)  # Text object will be rendered properly by Static

    def _build_graph(self, root_messages, session):
        """Build ASCII graph representation using Rich Text"""
        output = Text()

        # Header
        output.append("╔", style="bold blue")
        output.append("═" * 50, style="bold blue")
        output.append("╗\n", style="bold blue")
        output.append("║", style="bold blue")
        output.append(
            " " * 10 + "CONVERSATION FLOW DIAGRAM" + " " * 15, style="bold blue"
        )
        output.append("║\n", style="bold blue")
        output.append("╚", style="bold blue")
        output.append("═" * 50, style="bold blue")
        output.append("╝\n\n", style="bold blue")

        for idx, root in enumerate(root_messages):
            if idx > 0:
                output.append("\n" + "─" * 60 + "\n\n", style="dim")
            self._add_node_graph(
                root, session, output, level=0, is_last=True, prefix=""
            )

        return output

    def _add_node_graph(
        self, message, session, output, level=0, is_last=True, prefix=""
    ):
        """Recursively add nodes in flowchart style"""
        children = session.query(Message).filter_by(parent_id=message.id).all()

        if level == 0:
            connector = ""
            branch = ""
        else:
            connector = "└── " if is_last else "├── "
            branch = "    " if is_last else "│   "

        is_selected = self.current_message and message.id == self.current_message.id

        # Create message box
        self._create_message_box(
            message, is_selected, self.compact_mode, output, prefix, connector, branch
        )

        # Add children recursively
        for idx, child in enumerate(children):
            is_last_child = idx == len(children) - 1
            new_prefix = prefix + branch
            self._add_node_graph(
                child, session, output, level + 1, is_last_child, new_prefix
            )

    def _create_message_box(
        self, message, is_selected, compact, output, prefix, connector, branch
    ):
        """Create a box representation directly into the Text object"""

        # Determine style
        if message.speaker == "user":
            icon = "👤"
            color = "cyan"
        else:
            icon = "🤖"
            color = "green"

        if is_selected:
            color = f"bold {color}"

        timestamp = message.timestamp.strftime("%H:%M")

        # Content wrapping
        max_width = 50 if not compact else 30
        content_lines = self._wrap_text(message.content, max_width - 4)

        if compact and len(content_lines) > 2:
            content_lines = content_lines[:2]
            if len(content_lines[-1]) > max_width - 7:
                content_lines[-1] = content_lines[-1][: max_width - 7] + "..."

        width = max(len(line) for line in content_lines) + 4
        width = max(width, 25)

        # Top border
        output.append(prefix + connector)
        output.append("┌" + "─" * (width - 2) + "┐\n", style=color)

        # Header line
        output.append(prefix + branch)
        output.append("│ ", style=color)
        output.append(f"{icon} {message.speaker.upper()}", style=color)
        padding = width - len(f"{icon} {message.speaker.upper()}") - 4
        output.append(" " * padding)
        output.append(" │\n", style=color)

        # Timestamp line
        output.append(prefix + branch)
        output.append("│ ", style=color)
        timestamp_text = f"{timestamp} (ID:{message.id})"
        output.append(timestamp_text, style="dim")
        padding = width - len(timestamp_text) - 4
        output.append(" " * padding)
        output.append(" │\n", style=color)

        # Separator
        output.append(prefix + branch)
        output.append("├" + "─" * (width - 2) + "┤\n", style=color)

        # Content lines
        for line in content_lines:
            output.append(prefix + branch)
            output.append("│ ", style=color)
            output.append(line)
            padding = width - len(line) - 4
            output.append(" " * padding)
            output.append(" │\n", style=color)

        # Bottom border
        output.append(prefix + branch)
        output.append("└" + "─" * (width - 2) + "┘\n", style=color)

    def _wrap_text(self, text, width):
        """Wrap text to fit within width"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            word_length = len(word)
            if current_length + word_length + len(current_line) <= width:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length

        if current_line:
            lines.append(" ".join(current_line))

        return lines if lines else [""]

    def action_zoom_in(self):
        """Switch to detailed view"""
        self.compact_mode = False
        # Rebuild graph
        if hasattr(self, "app") and hasattr(self.app, "session"):
            self.show_graph(self.app.session, self.current_message)
        self.notify("Detailed view")

    def action_zoom_out(self):
        """Switch to compact view"""
        self.compact_mode = True
        # Rebuild graph
        if hasattr(self, "app") and hasattr(self.app, "session"):
            self.show_graph(self.app.session, self.current_message)
        self.notify("Compact view")

    def action_page_down(self):
        self.scroll_page_down()

    def action_page_up(self):
        self.scroll_page_up()
