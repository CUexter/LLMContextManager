# LLM Context Manager

A terminal user interface (TUI) for managing and compressing LLM chat context with support for branching conversations.

## Features

- **Tree-based message structure**: Navigate branching conversations with parent-child relationships
- **Multiple views**: Switch between tree view, conversation path view, and graph visualization
- **Vim-style navigation**: Intuitive keybindings (j/k/h/l/g/G) for efficient browsing
- **SQLite database**: Persistent storage of chat histories with SQLAlchemy ORM
- **LLM integration**: Built-in support for OpenAI and Anthropic APIs

## Installation

Requires Python >=3.13

### Using uv (recommended)

```bash
uv sync
```

### Using pip

```bash
pip install -e .
```

## Usage

### Running the application

```bash
python -m src.main
```

Or with uv:

```bash
uv run python -m src.main
```

### Custom database location

```bash
python -m src.main --db sqlite:///path/to/your/database.db
```

Default database location: `sqlite:///data/chat_history.db`

## Keybindings

### Global
- `q` - Quit application
- `r` - Refresh views
- `1` - Focus tree view
- `2` - Focus conversation/graph view
- `v` - Toggle between path and graph view
- `?` - Show help

### Tree Navigation (Vim-style)
- `j` / `↓` - Move down
- `k` / `↑` - Move up
- `h` / `←` - Collapse node / Move to parent
- `l` / `→` - Expand node / Move to first child
- `g` - Jump to top
- `G` - Jump to bottom

## Project Structure

```
src/
├── database/
│   ├── db.py           # Database initialization and session management
│   └── models.py       # SQLAlchemy models (Message with tree structure)
├── ui/
│   ├── app.py          # Main application class
│   ├── app.tcss        # Application styling
│   └── styles.py       # Style definitions
├── widgets/
│   ├── conversation_path.py    # Linear conversation path view
│   ├── graph_view.py           # Graph visualization of message tree
│   └── message_tree.py         # Tree widget for browsing messages
├── utils/
│   └── formatters.py           # Utility functions for formatting
└── main.py                     # Application entry point
```

## Development

### Code Style
- Python >=3.13
- Ruff for linting and formatting
- Snake_case for functions/variables, PascalCase for classes
- Explicit imports preferred

### Database Schema

The `Message` model supports tree-structured conversations:
- `id`: Primary key
- `parent_id`: Foreign key to parent message (nullable for root messages)
- `timestamp`: Message creation time
- `speaker`: 'user' or 'assistant'
- `content`: Message text
- `children`: One-to-many relationship to child messages

## License

MIT
