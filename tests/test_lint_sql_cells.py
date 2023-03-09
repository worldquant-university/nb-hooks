import nbformat
import pytest

from pre_commit_hooks.lint_sql_cells import clean_sql_cells, clean_sql_string

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

bad_bq_string = """%%bigquery --project $PROJECT
-- REMOVE{
select name from sqlite_schema where type="table"
-- REMOVE}
"""

good_bq_string = """%%bigquery --project $PROJECT

-- REMOVE{
SELECT name
FROM sqlite_schema
WHERE TYPE = "table"
-- REMOVE}"""


@pytest.fixture
def tmpfiles(tmpdir):
    # Create correct SQL file
    good_filename = tmpdir.join("good_sql.ipynb")
    good_nb = nbformat.v4.new_notebook()
    good_nb["cells"] = [
        nbformat.v4.new_code_cell(source=good_sql_string),
        nbformat.v4.new_code_cell(source=good_bq_string),
    ]
    with open(good_filename, "w") as f:
        nbformat.write(good_nb, f)

    # Create incorrect SQL file
    bad_filename = tmpdir.join("bad_sql.ipynb")
    bad_nb = nbformat.v4.new_notebook()
    bad_nb["cells"] = [
        nbformat.v4.new_code_cell(source=bad_sql_string),
        nbformat.v4.new_code_cell(source=bad_bq_string),
    ]
    with open(bad_filename, "w") as f:
        nbformat.write(bad_nb, f)
    yield tmpdir


def test_clean_sql_string():
    linted_sql_string = clean_sql_string(bad_sql_string)
    assert linted_sql_string == good_sql_string


def test_clean_sql_cells(tmpfiles):
    clean_sql_cells(tmpfiles.join("bad_sql.ipynb"))

    good_nb = nbformat.read(tmpfiles.join("good_sql.ipynb"), as_version=4)
    corrected_nb = nbformat.read(tmpfiles.join("bad_sql.ipynb"), as_version=4)

    good_source = [c["source"] for c in good_nb["cells"]]
    corrected_source = [c["source"] for c in corrected_nb["cells"]]

    print("GOOD")
    for x in good_source:
        print(x)

    print("CORRECTED")
    for x in corrected_source:
        print(x)

    assert all(gs == cs for gs, cs in zip(good_source, corrected_source))
