# Use Bash instead of PowerShell
set shell := ["bash", "-uc"]

# List available recipes
default:
    @just --list

# ------------------------------------------------------------------------------
# Project
# ------------------------------------------------------------------------------

# Set up the project for local development after cloning the repository
setup:
    uv sync --group dev
    uv run prek install --install-hooks
    uv run prek run --all-files
    uv run dbt deps
    uv run dbt debug
    @echo -----------------------------------------------
    @printf '\033[32m%s\033[0m\n' "Project setup complete."
    @echo -----------------------------------------------

# ------------------------------------------------------------------------------
# Git
# ------------------------------------------------------------------------------

# (git) Stage all changes
add:
    git add .

# (git) Amend the last commit
amend:
    git commit --amend

# (git) Delete a local merged branch (usage: just delete-branch feature/my-feature)
delete-branch name:
    git fetch --prune
    git branch -d {{name}}

# (git) Create a feature branch (usage: just feat my-feature)
feat name: main
    git switch -c feat/{{name}}

# (git) Create a fix branch (usage: just fix bug-123)
fix name: main
    git switch -c fix/{{name}}

# (git) Switch to main and pull latest changes
main:
    git switch main
    git pull --rebase origin main

# (git) Delete all local branches except main
cleanup: main
    git fetch --prune
    git branch --format='%(refname:short)' | while read -r branch; do \
        [[ "$$branch" == "main" ]] && continue; \
        git branch -D "$$branch"; \
    done
    @echo "All local branches removed except main."

# (git) Pull latest main into the current branch
pull:
    git pull --rebase origin main

# (git) Push the current branch
push: pull
    git push origin HEAD


# ------------------------------------------------------------------------------
# dbt
# ------------------------------------------------------------------------------

# (dbt) Install project dependencies
deps:
    dbt deps

# (dbt) Debug project configuration
debug:
    dbt debug

# (dbt) Build the project
build:
    dbt build --select dbt_databricks_project

# (dbt) Run the project
run:
    dbt run --select dbt_databricks_project


# ------------------------------------------------------------------------------
# Quality
# ------------------------------------------------------------------------------

# Run pre-commit hooks
lint:
    pre-commit run

# Run pre-commit hooks on all files
pre-commit:
    pre-commit run --all-files


# ------------------------------------------------------------------------------
# Python / uv
# ------------------------------------------------------------------------------

# Lock project dependencies
lock:
    uv lock

# Sync development dependencies
sync:
    uv sync --group dev


# ------------------------------------------------------------------------------
# Databricks
# ------------------------------------------------------------------------------

# (databricks) Authenticate with Databricks CLI
auth:
    databricks auth login

# (databricks) Validate the Databricks Asset Bundle
validate:
    databricks bundle validate

# (databricks) Deploy the Databricks Asset Bundle
deploy: validate
    databricks bundle deploy
