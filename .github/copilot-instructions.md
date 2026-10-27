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

Use `AGENTS.md` for repository context and the `code-review` skill for the
review workflow. Follow any applicable path-specific instructions in
`.github/instructions/`.
