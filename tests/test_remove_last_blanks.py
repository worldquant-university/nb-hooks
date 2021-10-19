from os import remove
import pytest

from pre_commit_hooks.remove_last_blanks import remove_empty_last_cells
from pre_commit_hooks.remove_last_blanks import main

def create_nb_fixture(add_blanks=False):
    nb = nbformat.v4.new_notebook()
    cells = [
        nbformat.v4.new_markdown_cell(source="Hello!"),
        nbformat.v4.new_code_cell(source="1+1"),
    ]
    if add_blanks:
        cells.append(nbformat.v4.new_markdown_cell(source=''))
        cells.append(nbformat.v4.new_markdown_cell(source=''))
    nb["cells"] = cells
    return nb

@pytest.fixture
def tmpfiles(tmpdir):
    file_path = tmpdir.join("correct.ipynb")
    with open(file_path, "w") as f:
        nbformat.write(create_nb(add_blanks=False), f)
    
    file_path = tmpdir.join("incorrrect.ipynb")
    with open(file_path, "w") as f:
        nbformat.write(create_nb(add_blanks=True), f)

    yield tmpdir

def remove_empty_last_cells(tmpfiles):
    remove_empty_last_cells(tmpfiles.join("correct.ipynb"))
    remove_empty_last_cells(tmpfiles.join("incorrrect.ipynb"))

    correct = nbformat.read(tmpfiles.join("correct.ipynb"), as_version=4)
    corrected = nbformat.read(tmpfiles.join("incorrrect.ipynb"), as_version=4)

    correct_source = [c["source"] for c in correct["cells"]]
    corrected_source = [c["source"] for c in corrected["cells"]]

    assert all(c == i for c, i in zip(correct_source, corrected_source))