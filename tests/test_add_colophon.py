import nbformat
import pytest

from pre_commit_hooks.add_colophon import add_colophon
from pre_commit_hooks.utils import copyright_text


def create_base_nb_fixture():
    nb = nbformat.v4.new_notebook()
    cells = [
        nbformat.v4.new_markdown_cell(source="Hello!"),
        nbformat.v4.new_markdown_cell(source=""),
        nbformat.v4.new_code_cell(source="1+1"),
        nbformat.v4.new_code_cell(source=""),
    ]
    nb["cells"] = cells
    return nb


@pytest.fixture
def tmpfiles(tmpdir):
    # Notebook where everything's correct
    filename = tmpdir.join("correct_colophon.ipynb")
    with open(filename, "w") as f:
        correct_nb = create_base_nb_fixture()
        correct_nb["cells"].append(nbformat.v4.new_markdown_cell(source=copyright_text))
        nbformat.write(correct_nb, f)

    # Notebook with copyright from different year
    filename = tmpdir.join("old_colophon.ipynb")
    with open(filename, "w") as f:
        old_colophon_nb = create_base_nb_fixture()
        old_colophon_nb["cells"].append(
            nbformat.v4.new_markdown_cell(source=copyright_text.replace("2021", "2020"))
        )
        nbformat.write(old_colophon_nb, f)

    # Notebook with no colophon
    filename = tmpdir.join("no_colophon.ipynb")
    with open(filename, "w") as f:
        no_colophon_nb = create_base_nb_fixture()
        nbformat.write(no_colophon_nb, f)

    yield tmpdir


def test_add_colophon(tmpfiles):
    files = ["correct_colophon.ipynb", "old_colophon.ipynb", "no_colophon.ipynb"]
    for f in files:
        add_colophon(tmpfiles.join(f))

    # Notebook cells against which three notebooks will be tested
    compare = create_base_nb_fixture()
    compare["cells"].append(nbformat.v4.new_markdown_cell(source=copyright_text))
    compare_source = [c["source"] for c in compare["cells"]]

    nbs = (nbformat.read(tmpfiles.join(f), as_version=4) for f in files)
    for nb in nbs:
        nb_source = [c["source"] for c in nb["cells"]]
        assert all([a == b for a, b in zip(compare_source, nb_source)])
