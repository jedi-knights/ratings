# Ratings

A repository to house ratings tools and functionality.

## Contributing

### Create a new library

Suppose you wanted to create a new library called base. Under the libs directory you would create it like so:

```shell
mkdir libs/base
touch Makefile
touch libs/base/README.md
touch libs/base/pyproject.toml
touch libs/base/requirments.txt

pushd libs/base
python3 -m venv .venv

# Make the virtual environment active
source .venv/bin/activate

# Install pinned pip first
pip install -r $(git rev-parse --show-toplevel)/pip-requirements.txt

# Install shared development dependencies and project/library specific dependencies
pip install -r $(git rev-parse --show-toplevel)/dev-requirements.txt -r requirements.txt
popd
```

With the library created, you can now type check your code using pyright.

```shell    
# With project-specific dependencies installed, you typecheck your code as follows:
pyright .
```