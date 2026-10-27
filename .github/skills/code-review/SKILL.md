---
name: code-review
description: Review pull request or local code changes for actionable correctness, data-quality, regression, and security issues. Use this skill when reviewing code changes.
---

# Code review workflow

1. Identify the base and proposed changes. Review the diff and enough
   surrounding code to understand affected behavior and existing conventions.
2. Trace changed logic through its callers, dbt dependencies, and relevant
   tests or configuration. Check whether the implementation matches the
   stated intent and whether edge cases can cause incorrect results or
   failures.
3. For dbt model changes, establish the intended grain and follow the relevant
   `source()` and `ref()` lineage. Check join cardinality, aggregation,
   filtering, null handling, incremental behavior if present, and consistency
   of YAML documentation and tests with the SQL.
4. Report only concrete, actionable defects introduced by the changes. For
   each, give a concise explanation of impact and trigger conditions, and
   cite the smallest relevant changed line range. Order findings by severity.
5. Do not modify files as part of a review. Do not infer correctness from
   formatting or parsing alone. If validation commands are available and
   relevant, state clearly whether they were run and what they establish.
6. If no actionable defects are supported by the evidence, state that there
   are no findings. Mention meaningful uncertainty rather than guessing.
