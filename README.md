[![Tests](https://github.com/worldquant-university/nb-hooks/workflows/Tests/badge.svg)](https://github.com/worldquant-university/nb-hooks/actions)

# Notebook Hooks

Some hooks the staff at WorldQuant University use for keeping our curriculum tidy and consistent.

## Using nb-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-  repo: https://github.com/pre-commit/pre-commit-hooks
   rev: main
   hooks:
   - id: remove-last-blanks
   - id: lint-sql-cells
```

## Hooks Available

### `remove-last-blanks`

Removes empty cells from the end of a notebook.

### `lint-sql-cells`

Lints all code cells that begin with `%%sql` (uses [`sqlparse`](https://github.com/andialbrecht/sqlparse)).
