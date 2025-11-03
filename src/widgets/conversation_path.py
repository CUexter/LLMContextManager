"""Widget for displaying conversation paths"""

from pathlib import Path
from textual.widgets import Static
from textual.containers import ScrollableContainer
from textual.binding import Binding

from src.database.models import Message
from src.utils.formatters import format_message_detail


class ConversationPath(ScrollableContainer):
    """Widget to show the full conversation path from root to selected message"""

    # Load CSS from same directory
    CSS_PATH = Path(__file__).with_suffix(".tcss")

    BINDINGS = [
        Binding("j", "scroll_down", "Down", show=False),
        Binding("k", "scroll_up", "Up", show=False),
        Binding("g", "scroll_home", "Top", show=False),
        Binding("G", "scroll_end", "Bottom", show=False),
        Binding("d", "page_down", "Page Down", show=False),
        Binding("u", "page_up", "Page Up", show=False),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_message = None

    def compose(self):
        """Compose initial widget with placeholder"""
        yield Static(
            "📋 Select a message from the tree to view conversation path",
            classes="placeholder",
        )

    def show_conversation_path(self, message: Message, session):
        """Display the full conversation path leading to this message"""
        self.current_message = message

        try:
            path = message.get_path_from_root(session)

            # Remove old widgets
            for widget in self.query(
                ".conv-header, .message-box, .arrow, .placeholder"
            ):
                widget.remove()

            # Add header
            header = Static(
                f"📋 Conversation Path — {len(path)} messages",
                classes="conv-header",
            )
            self.mount(header)

            # Add each message
            for idx, msg in enumerate(path):
                self._add_message_display(msg, idx, len(path))

        except Exception as e:
            self.log(f"Error: {e}")
            import traceback

            self.log(traceback.format_exc())

            error_widget = Static(f"⚠️  Error: {e}", classes="error")
            self.mount(error_widget)

    def _add_message_display(self, message: Message, index: int, total: int):
        """Add a single message to the conversation view"""
        try:
            content_text, _ = format_message_detail(message)

            # Build classes
            classes = ["message-box", message.speaker]
            if message == self.current_message:
                classes.append("selected")

            msg_static = Static(content_text, classes=" ".join(classes))
            self.mount(msg_static)

            # Add arrow between messages
            if index < total - 1:
                arrow = Static("⬇️", classes="arrow")
                self.mount(arrow)

        except Exception as e:
            self.log(f"Error adding message: {e}")

    def action_page_down(self) -> None:
        self.scroll_page_down()

    def action_page_up(self) -> None:
        self.scroll_page_up()
