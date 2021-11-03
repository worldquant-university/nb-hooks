[![Tests](https://github.com/worldquant-university/nb-hooks/workflows/Tests/badge.svg)](https://github.com/worldquant-university/nb-hooks/actions)

# Notebook Hooks

Some hooks the staff at WorldQuant University use for keeping our curriculum tidy and consistent.

## Using nb-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-  repo: https://github.com/pre-commit/pre-commit-hooks
   rev: main
   hooks:
   - id: remove-blank-cells
   - id: lint-sql-cells
   - id: add-colophon
   - id: add-task-numbers
```

## Hooks Available

### `remove-blank-cells`

Removes empty cells from notebook.

### `lint-sql-cells`

Lints all code cells that begin with `%%sql` (uses [`sqlparse`](https://github.com/andialbrecht/sqlparse)).

### `add-colophon`

Adds or corrects copyright cell at end of notebook.

### `add-task-numbers`

For notebooks that have tasks in markdown cells (denoted by `**Task:**`),
adds or corrects task numbering.
