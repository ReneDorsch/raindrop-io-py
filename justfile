set dotenv-load

# The list of available targets
default:
    @just --list

################################################################################
# Packaging...
################################################################################
# Build *and* publish to PyPI
publish:
    poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
    @rm -rf build raindroppy.egg-info

################################################################################
# Development...
################################################################################
# Run the raindrop-io-py command-line interface
cli:
    python raindroppy/cli/cli.py

# Run tests
test *args:
    python -m pytest {{args}}

# Pre-commit - Run all
pre-commit-all *args:
    pre-commit run --all-files {{args}}

# Pre-commit - Update new configuration and run
pre-commit-update *args:
    pre-commit install
    git add .pre-commit-config.yaml
    just pre-commit-all {{args}}

# Run samples against live Raindrop environment (assumes RAINDROP_TOKEN in env!)
examples:
    # Listed in order of complexity, list_* are read-only, rest make changes.
    # We try to be nice to Raindrop by resting between each file.
    python examples/list_authorised_user.py
    @echo "Sleeping..."
    @sleep 1

    python examples/list_collections.py
    @echo "Sleeping..."
    @sleep 1

    python examples/list_tags.py
    @echo "Sleeping..."
    @sleep 1

    python examples/create_collection.py
    @echo "Sleeping..."
    @sleep 1

    python examples/edit_collection.py
    @echo "Sleeping..."
    @sleep 1

    python examples/create_raindrop_file.py
    @echo "Sleeping..."
    @sleep 1

    python examples/create_raindrop_link.py
    @echo "Sleeping..."
    @sleep 1

    python examples/edit_raindrop.py
    @echo "Sleeping..."
    @sleep 1

    python examples/search_raindrop.py
