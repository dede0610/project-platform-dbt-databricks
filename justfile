# use sh instead of PowerShell:
set shell := ["bash", "-c"]

# List available just commands (default)
default:
  @just --list

# Activate the virtual environment
activate:
  .venv\Scripts\Activate.ps1

# (git) Stage all changes
add:
  git add .

# (git) Amend the last commit
amend:
  git commit --amend

# (databricks) Authenticate with Databricks CLI
auth:
  databricks auth login

# (dbt) Build the dbt project
build:
  dbt build -s dbt_databricks_project


# (databricks) DAB validate
db-validate:
  databricks bundle validate

# (databricks) DAB deploy
db-deploy:
  databricks bundle deploy


# (git) Initialize environment after clone
clone:
  uv venv
  just activate
  just sync
  pre-commit install --install-hooks
  dbt init

# (git) Commit changes with commitizen
commit:
  cz commit

# (dbt) Debug the dbt project
debug:
  dbt debug

# (git) Delete local (merged) branch (usage: just delete-branch feature/my-feature)
delete-branch name:
  just prune
  git branch -d {{name}}

# (databricks) Deploy the Databricks Asset Bundle
deploy: validate
  databricks bundle deploy

# (dbt) Install dbt project dependencies
deps:
  dbt deps

# (git) Create a feature branch with prefix (usage: just feat my-feature)
feat name:
  @just main
  git checkout -b feature/{{name}}

# (git) Create a fix branch with prefix (usage: just fix bug-123)
fix name:
  @just main
  git checkout -b fix/{{name}}

# Initialize a new project after copying the template
init:
  git init
  uv venv
  just activate
  just sync
  git add .
  git commit -m "feat: initial commit"
  pre-commit install --install-hooks
  just pre-commit
  dbt init

# Lint the dbt project
lint:
  pre-commit run

# (git) List local branches
list-branches:
  git branch -l

# Lock project dependencies
lock:
  uv lock

# (git) Switch to main branch and pull latest changes
main:
  git checkout main
  just pull

# (git) Run pre-commit hooks on all files
pre-commit:
  pre-commit run --all-files

# (git) Sync and prune local tracking branches
prune:
  git fetch --prune
  @echo "Remote branches pruned. Use 'git branch -d' for local cleanup."

# (git) Pull changes from the remote repository
pull:
  git pull --rebase origin main

# (git) Push changes to the remote repository
push: pull
  git push origin HEAD

# (dbt) Run the dbt project
run:
  dbt run --select dbt_databricks_project

# Sync project dependencies to the virtual environment
sync:
  uv sync --group dev

# Update the project with the latest template version
update:
  uvx copier update --skip-answered

# (databricks) Update databricks CLI to the latest version (usage: just update-databricks-cli)
update-databricks-cli:
  winget upgrade Databricks.DatabricksCLI --version 0.287.0

# (databricks) Validate the Databricks Asset Bundle
validate:
  databricks bundle validate
