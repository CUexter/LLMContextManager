"""CSS styles for the application"""

APP_CSS = """
Screen {
    layout: horizontal;
}

#tree-container {
    width: 35%;
    border: solid green;
}

#view-container {
    width: 65%;
    border: solid blue;
}

MessageTree {
    height: 100%;
}

ConversationPath {
    height: 100%;
    background: $surface;
}

GraphView {
    height: 100%;
    background: $surface;
}

.graph-content {
    height: auto;
    padding: 1;
}

TabbedContent {
    height: 100%;
}

TabPane {
    height: 100%;
}

.conv-header {
    background: $primary;
    padding: 1;
    margin-bottom: 1;
}

.message-box {
    border: solid;
    padding: 1;
    margin: 1;
    background: $surface-darken-1;
}

.message-box.user {
    border: solid cyan;
}

.message-box.assistant {
    border: solid green;
}

.arrow {
    text-align: center;
    color: $text-muted;
    margin: 0 0 1 0;
}

/* Tab styling */
Tabs {
    background: $primary;
}

Tab {
    padding: 0 2;
}

Tab.-active {
    background: $accent;
    text-style: bold;
}
/* Make sure conversation path is visible */
ConversationPath {
    height: 100%;
    background: $surface;
    border: solid yellow;  /* DEBUG: Make it obvious */
}

.placeholder {
    padding: 2;
    background: orange;  /* DEBUG: Very visible */
    color: black;
}

.conv-header {
    background: $primary;
    padding: 1;
    margin-bottom: 1;
}

.message-box {
    border: solid;
    padding: 1;
    margin: 1;
    background: $surface-darken-1;
    min-height: 5;  /* Make sure it has height */
}

.message-box.user {
    border: solid cyan;
}

.message-box.assistant {
    border: solid green;
}

.arrow {
    text-align: center;
    color: $text-muted;
    margin: 0 0 1 0;
    height: 3;  /* Make sure arrow has height */
}

.error {
    background: red;
    color: white;
    padding: 2;
}
"""
