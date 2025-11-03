"""Tree widget for displaying chat message hierarchy"""

from pathlib import Path
from textual.widgets import Tree
from textual.binding import Binding

from src.database.models import Message
from src.utils.formatters import format_message_label


class MessageTree(Tree):
    """Custom Tree widget for displaying chat messages with Vim bindings"""

    # Load CSS from same directory - just change extension!
    CSS_PATH = Path(__file__).with_suffix(".tcss")

    BINDINGS = [
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("h", "collapse_node", "Collapse", show=False),
        Binding("l", "expand_node", "Expand", show=False),
        Binding("g", "scroll_home", "Top", show=False),
        Binding("G", "scroll_end", "Bottom", show=False),
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("space", "toggle_node", "Toggle", show=False),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__("Chat History", *args, **kwargs)
        self.show_root = True
        self.guide_depth = 4

    def action_collapse_node(self) -> None:
        if self.cursor_node:
            if self.cursor_node.is_expanded:
                self.cursor_node.collapse()
            elif self.cursor_node.parent:
                self.cursor_node = self.cursor_node.parent

    def action_expand_node(self) -> None:
        if self.cursor_node:
            if not self.cursor_node.is_expanded and self.cursor_node.allow_expand:
                self.cursor_node.expand()
            elif self.cursor_node.children:
                self.cursor_node = self.cursor_node.children[0]

    def action_toggle_node(self) -> None:
        if self.cursor_node:
            self.cursor_node.toggle()

    def build_tree_from_db(self, session):
        self.clear()
        root_messages = session.query(Message).filter_by(parent_id=None).all()

        for root_msg in root_messages:
            self._add_message_node(self.root, root_msg, session)

        self.root.expand()

    def _add_message_node(self, parent_node, message, session):
        label = format_message_label(message)
        node = parent_node.add(label, data=message)

        children = session.query(Message).filter_by(parent_id=message.id).all()

        for child in children:
            self._add_message_node(node, child, session)
