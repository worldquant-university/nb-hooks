import pytest
import nbformat
import sqlparse

from pre_commit_hooks.lint_sql_cells import clean_sql_string

bad_sql_string = """%%sql
-- REMOVE{
select name from sqlite_schema where type="table"
-- REMOVE}"""

good_sql_string = """%%sql
-- REMOVE{
SELECT name
FROM sqlite_schema
WHERE TYPE = "table"
-- REMOVE}"""

def test_clean_sql_string():
    linted_sql_string = clean_sql_string(bad_sql_string)
    assert linted_sql_string == good_sql_string