# Agent Guidelines for LLM Context Manager

## Build/Run Commands
- **Run app**: `python -m src.main` or `uv run python -m src.main`
- **Install deps**: `uv sync`
- **Database**: Default is `sqlite:///data/chat_history.db`, configurable via `--db` flag
- **No tests found**: Project has no test suite yet

## Code Style
- **Python version**: >=3.13 (see pyproject.toml)
- **Imports**: Explicit imports preferred (see app.py:8-14). Use `from src.module import Class` style
- **Formatting**: Ruff configured but no strict rules defined
- **Type hints**: Not consistently used; add when beneficial but match existing code
- **Docstrings**: Use triple-quote docstrings for modules/classes/functions (see existing files)
- **Naming**: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants

## Architecture
- **Database**: SQLAlchemy models in `src/database/` (Message model with tree structure via parent_id)
- **UI**: Textual TUI framework in `src/ui/` and `src/widgets/`
- **Bindings**: Vim-style keybindings (j/k/h/l/g/G) for navigation (see MessageTree, app.py)
- **Session management**: Pass `session` parameter to methods that need DB access

## Error Handling
- No explicit error handling patterns observed; follow standard Python practices
