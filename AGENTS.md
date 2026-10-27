# Repository guide

## Project

This repository is a dbt Core project for Databricks, based on the Jaffle Shop
sample data. It demonstrates analytics engineering and a Databricks platform
workflow, including CI/CD, environment-specific deployments, and a Streamlit
data browser. The project uses Python 3.12, dbt Core 1.12, and Databricks.

## Where things live

- `src/` is the dbt project: models, seeds, macros, tests, and dbt config.
- `src/models/staging/` contains source-aligned staging views.
- `src/models/marts/` contains curated data marts, materialized as tables.
- `streamlit/` contains the data browser application.
- `resources/` and `databricks.yml` define Databricks Asset Bundles.
- `.dbt/` contains local dbt profiles; do not commit credentials.
- `.github/workflows/` contains CI and deployment workflows.
- `justfile` documents common development commands.

## Development and validation

Use the repository's `justfile` as the command reference:

- `just sync` syncs Python dependencies with `uv`.
- `uv run dbt deps --project-dir src` installs dbt packages.
- `uv run dbt parse --project-dir src --profiles-dir .dbt --target dev`
  parses the dbt project. Parsing does not connect to Databricks.
- `uv run dbt test --project-dir src --profiles-dir .dbt --target ci --select test_type:unit`
  runs dbt unit tests; this target requires configured Databricks credentials
  and access.
- `just pre-commit` runs pre-commit hooks across all files.
- `just validate` validates the Databricks bundle and requires Databricks
  configuration.

The PR workflow also checks the PR title, changed-file YAML/TOML and whitespace
hooks, SQL formatting, dbt parsing, dbt unit tests, Python types, and bundle
validation. Some checks need repository secrets and are skipped for forked PRs.

## Project conventions

- Preserve the staging-to-marts layering and use dbt `source()` and `ref()` to
  express dependencies.
- Keep model documentation and data tests alongside models in YAML. Document
  each model's grain and important columns; add or update tests when behavior
  or data guarantees change.
- Staging models are views in the `stg` schema; marts are tables in the
  `curated` schema. Seeds use the `raw` schema. Check the dbt project config
  before changing materialization or schema behavior.
- Follow existing SQL formatting and Jinja conventions; `sqlfmt` is used in
  CI.
- Do not put credentials, tokens, or other secrets in code, configuration, or
  generated documentation.
