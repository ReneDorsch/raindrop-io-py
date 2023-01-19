set dotenv-load

# The list of available targets
default:
    @just --list

################################################################################
# Usage
################################################################################
# Run our command-line interface
cli:
    python -m raindroppy.cli

#(old way:)
#    python raindrop/cli/cli.py {{args}}

################################################################################
# Development support...
################################################################################
# Run local unit tests (fast, no connection or Raindrop.io configuration required)
test *args:
    python -m pytest {{args}}

# Update the repo to the most recent .pre-commit-config.yaml and run it.
pre-commit-update *args:
    pre-commit install
    git add .pre-commit-config.yaml
    pre-commit run --all-files {{args}}

sleep:
    @echo "Waiting..."
    @sleep 1

# Run samples against live Raindrop environment (assumes RAINDROP_TOKEN in env!)
run_examples:
    # Listed in order of complexity, list_* are read-only, rest make changes.
    # Be nice to Raindrop and rest in between each one.
    python examples/list_authorised_user.py
    just sleep
    python examples/list_collections.py
    just sleep
    python examples/list_tags.py
    just sleep
    python examples/create_collection.py
    just sleep
    python examples/edit_collection.py
    just sleep
    python examples/create_raindrop_file.py
    just sleep
    python examples/create_raindrop_link.py
    just sleep
    python examples/edit_raindrop.py
    just sleep
    python examples/search_raindrop.py

################################################################################
# Packaging support...
################################################################################
# Clean our build enviroment:
clean:
    @echo "🚀 Cleaning house..."
    @rm -rf dist

# Build our package..
build:
    just clean
    @echo "🚀 Building..."
    @poetry build

# Build and publish
build_and_publish:
    just build
    just publish

# Publish our build to *TestPyPi* (args: --dry-run for example)
publish *args:
    poetry publish --repository testpypi --username $PYPI_TEST_USERNAME --password $PYPI_TEST_PASSWORD {{args}}

# Publish our build to *production* PyPi:
publish_production:
    echo "🚀 Publishing: Dry run..."
    poetry config pypi-token.pypi $(PYPI_TOKEN)
    poetry publish --dry-run
    echo "🚀 Publishing..."
    poetry publish
