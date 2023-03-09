import nbformat
import pytest

from pre_commit_hooks.remove_blank_cells import remove_blank_cells


def create_nb_fixture(add_blanks=False):
    nb = nbformat.v4.new_notebook()
    cells = [
        nbformat.v4.new_markdown_cell(source="Hello!"),
        nbformat.v4.new_code_cell(source="1+1"),
        nbformat.v4.new_markdown_cell(source="        Hello!"),
        nbformat.v4.new_code_cell(source="\n\n\n1+1\n\n"),
    ]
    if add_blanks:
        cells.append(nbformat.v4.new_markdown_cell(source=""))
        cells.append(nbformat.v4.new_markdown_cell(source=""))
    nb["cells"] = cells
    return nb


@pytest.fixture
def tmpfiles(tmpdir):
    file_path = tmpdir.join("correct.ipynb")
    with open(file_path, "w") as f:
        nbformat.write(create_nb_fixture(add_blanks=False), f)

    file_path = tmpdir.join("incorrrect.ipynb")
    with open(file_path, "w") as f:
        nbformat.write(create_nb_fixture(add_blanks=True), f)

    yield tmpdir


def test_remove_blank_cells(tmpfiles):
    remove_blank_cells(tmpfiles.join("correct.ipynb"))
    remove_blank_cells(tmpfiles.join("incorrrect.ipynb"))

    correct = nbformat.read(
        tmpfiles.join("correct.ipynb"), as_version=nbformat.NO_CONVERT
    )
    corrected = nbformat.read(
        tmpfiles.join("incorrrect.ipynb"), as_version=nbformat.NO_CONVERT
    )

    correct_source = [c["source"] for c in correct["cells"]]
    corrected_source = [c["source"] for c in corrected["cells"]]

    assert all(c == i for c, i in zip(correct_source, corrected_source))
