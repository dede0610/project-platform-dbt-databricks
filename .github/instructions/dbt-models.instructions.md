---
applyTo: "src/models/**/*.sql,src/models/**/*.yml"
---

When reviewing dbt model changes, verify the documented grain against the SQL
and check whether joins can duplicate or drop records. Check aggregation
levels, filter placement, null handling, units and casts, and the correctness
of `source()` and `ref()` dependencies.

Staging models in this project are views in `stg`; marts are tables in
`curated`. Preserve those conventions unless the change intentionally updates
the dbt configuration and deployment expectations as well.

For behavioral changes, check that model and column descriptions, generic data
tests, and unit tests still describe the new behavior. Do not consider a
successful parse or formatting check proof of data correctness.
