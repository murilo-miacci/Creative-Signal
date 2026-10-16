set shell := ["bash", "-eu", "-c"]
set positional-arguments

# Show available commands
[group('commands')]
default:
    @just --list

# First-time setup & Update
[group('setup')]
setup:
    @echo ""
    @echo "Syncing project virtual environment with uv..."
    @uv sync --locked
    @echo ""
    @echo "✓ Setup complete!"
    @echo ""

# Runs the exploratory data analysis
[group('exe')]
eda:
    @uv run --locked python src/eda.py

# Runs the model training
[group('exe')]
train:
    @uv run --locked python src/train.py

# Auto-format every Python file with ruff
[group('quality')]
format:
    @echo "Formatting code with ruff..."
    @uv run --locked ruff format src tests

# Run all linters in sequence
[group('quality')]
lint:
    @echo ""
    @echo "===== Ruff ====="
    uv run --locked ruff check src tests
    @echo ""
    @echo "===== Pylint ====="
    uv run --locked pylint src tests
    @echo ""
    @echo "===== Mypy ====="
    uv run --locked mypy src tests
    @echo ""
    @echo "✓ All linters passed"

# Run the test suite
[group('quality')]
test:
    @echo "Running tests..."
    @uv run --locked pytest -q

[group('Recommendation Engine')]
recommend campaign-id:
    @uv run --locked python src/recommend.py --campaign_id "$1"