# Copilot review guidance

Review the proposed changes for concrete defects, prioritizing incorrect data,
broken behavior, regressions, and security or privacy risks. Report only
actionable findings that the author can fix; do not report preferences, issues
that are merely hypothetical, or findings already addressed by the diff.

For each finding, explain the impact and the conditions needed to trigger it.
Point to the smallest relevant changed line range. If no actionable issue is
found, say so without inventing concerns. Do not treat this review as a
replacement for CI or human approval.

For dbt changes, pay particular attention to model grain, join cardinality,
aggregation, null behavior, source/ref dependencies, and whether model
documentation and data tests remain accurate. Do not assume a SQL change is
correct just because it parses or is formatted.

Use `AGENTS.md` for repository context and the `code-review-and-quality` skill for the
review workflow. Follow any applicable path-specific instructions in
`.github/instructions/`.

## Project architecture

This repository deploys a dbt analytics project and a small Streamlit data browser to Databricks. `databricks.yml` defines local, dev, tst, and prd bundle targets; bundle resources define the dbt job and Streamlit app. The job installs dbt packages, loads CSV seeds, and builds the project. CI parses dbt without a workspace connection, while unit tests and bundle validation use Databricks credentials.

The dbt project is under `src/`. CSV seeds create raw tables; staging models clean and reshape those sources; marts combine them into curated tables. The Databricks job runs the resulting project in an environment-specific Unity Catalog catalog. The Streamlit app reads the curated customers model through a SQL warehouse, choosing the catalog from its deployed app name.

Deployments promote merged changes to dev, releases to tst, and manually selected releases to prd. The production deployment also publishes dbt documentation for that release.

## Build, test, and lint

Run commands from the repository root. Set up Python 3.12 and dependencies with `uv sync --group dev`. Install dbt packages with `uv run dbt deps --project-dir src`.

| Purpose | Command |
| --- | --- |
| Parse dbt without connecting to Databricks | `uv run dbt parse --project-dir src --profiles-dir .dbt --target dev` |
| Load seeds in a configured workspace | `uv run dbt seed --project-dir src --profiles-dir .dbt --target dev` |
| Build models and run their data tests | `uv run dbt build --project-dir src --profiles-dir .dbt --target dev` |
| Run all dbt unit tests | `uv run dbt test --project-dir src --profiles-dir .dbt --target ci --select test_type:unit` |
| Run one dbt unit test | `uv run dbt test --project-dir src --profiles-dir .dbt --target ci --select 'test_type:unit,test_supply_costs_sum_correctly'` |
| Check SQL formatting for one file | `uv run sqlfmt --diff src/models/marts/orders.sql` |
| Run all pre-commit hooks | `just pre-commit` |
| Check Streamlit Python types | `uv run --project streamlit --with ty ty check streamlit/*.py` |
| Check types in one Streamlit file | `uv run --project streamlit --with ty ty check streamlit/app.py` |
| Validate the Databricks bundle | `just validate` |

Replace the example unit-test name or SQL path with the one being changed. dbt unit tests require Databricks credentials and workspace access; `dbt parse` does not. Bundle validation also needs Databricks configuration.

## Repository conventions

- Keep dbt dependencies explicit with `source()` for seeded/source data and `ref()` for models. Staging models are views in `stg`, marts are tables in `curated`, and seeds use `raw`. `src/macros/dbt_overrides/generate_schema_name.sql` uses a custom schema as-is rather than appending it to the target schema.
- Keep model and column descriptions, grain, generic data tests, and unit tests alongside the model in YAML. Unit tests use fixture rows for their `source()` and `ref()` inputs. For changes to joins or aggregations, verify row grain and cardinality as well as totals and null behavior.
- SQL formatting and linting are configured in `pyproject.toml` and run by pre-commit; use lowercase SQL keywords/functions and single-quoted string literals, consistent with the SQLFluff configuration.
- Streamlit dependencies are managed separately in `streamlit/pyproject.toml`. Its Databricks connection uses the SDK's default authentication and the configured SQL warehouse; do not hard-code credentials.
- Databricks credentials belong in local profiles or GitHub environment secrets, never in source, bundle configuration, or generated documentation.
- Use Conventional Commit messages; the commit-msg hook validates them.
