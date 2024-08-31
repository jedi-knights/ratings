# .zshrc

# Activate the virtual environment
source .venv/bin/activate

export PYTHONPATH=$(git rev-parse --show-toplevel):$PYTHONPATH
