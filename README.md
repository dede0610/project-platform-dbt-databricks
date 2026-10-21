[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/downloads/windows/)
![Databricks](https://img.shields.io/badge/platform-Databricks-orange?logo=databricks)
![dbt Core](https://img.shields.io/badge/platform-dbt%20Core-orange)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

# project-platform-dbt-databricks
> This project uses the dbt Jaffle Shop sample data to build a simple data product on Databricks (free edition). The primary goal is not the data model itself, but to demonstrate how modern analytics engineering practices can be implemented on the Databricks platform using dbt.

The project explores:

- dbt development and deployment on Databricks
- Databricks Asset Bundles for infrastructure and workload management
- Source control and deployment best practices
- Pull request based development workflow
- Automated release management with Release Please
- CI/CD automation using GitHub Actions
- Automated testing and deployment across environments
- Service Principal authentication instead of personal credentials

## 🧪 Technologies
- Python 3.12
- Azure Databricks Serverless
- Unity Catalog
- Databricks Asset Bundles
- Lakeflow Jobs
- dbt Core 1.12.5
- Visual Studio Code (GitHub Codespace)
- Pre-commit
- Commitizen
- uv
- ruff
- sqlfmt
- SQLFluff
- Just
- GitHub Actions
- Dependabot

## 📦 Features
### Analytics Engineering
- dbt Core project based on the Jaffle Shop dataset
- Layered transformation approach (raw, staging, marts)
- Automated data quality testing
- Documentation generation

### Platform & Deployment
- Databricks Asset Bundles (DAB)
- Environment-specific deployments (Dev, Test, Prod)
- Service Principal authentication
- Databricks Workflows orchestration

### DevOps
- GitHub Actions CI/CD pipelines
- Pull request validation checks
- Automated deployment promotion
- Release Please automated versioning and changelog management
- Git-based development workflow

## Getting Started
### 📦 Pre-requsites
* [uv](https://docs.astral.sh/uv/) - `py -m pip install uv`
* git
* [Databricks CLI](https://github.com/databricks/cli)
* Just - `uv tool install rust-just`
