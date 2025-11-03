"""Main application class"""

from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TabbedContent, TabPane
from textual.containers import Horizontal, Vertical
from textual.binding import Binding

from src.database.models import Message
from src.database.db import init_db, create_sample_data
from src.widgets.message_tree import MessageTree
from src.widgets.conversation_path import ConversationPath
from src.widgets.graph_view import GraphView


class ChatManagerApp(App):
    """Main TUI application for managing chat history"""

    # Load app CSS
    CSS_PATH = Path(__file__).with_suffix(".tcss")

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("1", "focus_tree", "Focus Tree", show=True),
        Binding("2", "focus_view", "Focus View", show=True),
        Binding("v", "toggle_view", "Toggle View", show=True),
        Binding("?", "help", "Help", show=True),
    ]

    def __init__(self, db_url="sqlite:///data/chat_history.db"):
        super().__init__()
        self.db_url = db_url
        self.session = init_db(self.db_url)

        if self.session.query(Message).count() == 0:
            create_sample_data(self.session)

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            with Vertical(id="tree-container"):
                yield MessageTree(id="message-tree")

            with Vertical(id="view-container"):
                with TabbedContent(initial="path-tab"):
                    with TabPane("Path View", id="path-tab"):
                        yield ConversationPath(id="conversation-path")

                    with TabPane("Graph View", id="graph-tab"):
                        yield GraphView(id="graph-view")

        yield Footer()

    def on_mount(self) -> None:
        tree = self.query_one("#message-tree", MessageTree)
        tree.build_tree_from_db(self.session)

        first_message = self.session.query(Message).first()
        if first_message:
            conversation = self.query_one("#conversation-path", ConversationPath)
            conversation.show_conversation_path(first_message, self.session)

            graph = self.query_one("#graph-view", GraphView)
            graph.show_graph(self.session, first_message)

        tree.focus()

    def on_tree_node_highlighted(self, event) -> None:
        if event.node.data:
            conversation = self.query_one("#conversation-path", ConversationPath)
            conversation.show_conversation_path(event.node.data, self.session)

            graph = self.query_one("#graph-view", GraphView)
            graph.show_graph(self.session, event.node.data)

    def action_refresh(self) -> None:
        tree = self.query_one("#message-tree", MessageTree)
        tree.build_tree_from_db(self.session)

        graph = self.query_one("#graph-view", GraphView)
        graph.show_graph(self.session)

        self.notify("Refreshed")

    def action_focus_tree(self) -> None:
        self.query_one("#message-tree").focus()

    def action_focus_view(self) -> None:
        tabs = self.query_one(TabbedContent)
        if tabs.active == "path-tab":
            self.query_one("#conversation-path").focus()
        else:
            self.query_one("#graph-view").focus()

    def action_toggle_view(self) -> None:
        tabs = self.query_one(TabbedContent)
        tabs.active = "graph-tab" if tabs.active == "path-tab" else "path-tab"

    def action_help(self) -> None:
        self.notify("Press ? for help", timeout=5)

    def on_unmount(self) -> None:
        self.session.close()
