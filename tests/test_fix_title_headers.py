import nbformat
import pytest

from pre_commit_hooks.fix_title_headers import check_for_title
from tests.conftest import save_nb


# Three fixtures
# 1. CORRECT: First cell markdown w/ title formatting, no other text
# 2. First cell isn't markdown
# 3. First cell is markdown, but no title formatting
# 4. First cell is markdown w/ title formatting, but other text in cell
@pytest.fixture
def tmpfiles(tmpdir):
    base_nb = nbformat.v4.new_notebook()
    # 1. Correct
    nb_1_file = tmpdir.join("001-correct-title.ipynb")
    base_nb["cells"] = [
        nbformat.v4.new_markdown_cell(
            source='<font size="+3"><strong>Getting started with Python</strong></font>'
        )
    ]
    save_nb(base_nb, nb_1_file)

    # 2. First cell isn't markdown
    nb_2_file = tmpdir.join("002-first-cell-code.ipynb")
    base_nb["cells"] = [
        nbformat.v4.new_code_cell(source="1+1"),
        nbformat.v4.new_markdown_cell(
            source='<font size="+3"><strong>Getting started with Python</strong></font>'
        ),
    ]
    save_nb(base_nb, nb_2_file)

    # 3. First cell is markdown, but no title formatting
    nb_3_file = tmpdir.join("003-bad-title.ipynb")
    base_nb["cells"] = [
        nbformat.v4.new_markdown_cell(source="# Getting started with Python")
    ]
    save_nb(base_nb, nb_3_file)

    # 4. First cell is markdown w/ title formatting, but other text in cell
    nb_4_file = tmpdir.join("004-other-text.ipynb")
    base_nb["cells"] = [
        nbformat.v4.new_markdown_cell(
            source="""<font size="+3"><strong>Getting started with Python</strong></font>

            Welcome to our amazing course!"""
        )
    ]
    save_nb(base_nb, nb_4_file)

    yield tmpdir


def test_check_for_title(tmpfiles):
    assert check_for_title(tmpfiles.join("001-correct-title.ipynb")) == 0
    assert check_for_title(tmpfiles.join("002-first-cell-code.ipynb")) == 1
    assert check_for_title(tmpfiles.join("003-bad-title.ipynb")) == 1
    assert check_for_title(tmpfiles.join("004-other-text.ipynb")) == 1
