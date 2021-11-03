import nbformat
import pytest

from pre_commit_hooks.add_task_numbers import add_task_numbers


def save_nb(nb, filename):
    with open(filename, "w") as f:
        nbformat.write(nb, f)


def get_source_from_file(filename):
    nb = nbformat.read(filename, as_version=4)
    return [c["source"] for c in nb["cells"]]


# Three fixtures
# 1. Notebook with correct numbering
# 2. Notebook with no numbering
# 3. Notebook with incorrect numbering
@pytest.fixture
def tmpfiles(tmpdir):
    # Notebook with correct numbering
    correct_num_fn = tmpdir.join("011-correct-num.ipynb")
    correct_num_nb = nbformat.v4.new_notebook()
    correct_num_nb["cells"] = [
        nbformat.v4.new_markdown_cell(source="**Task 11.1:**"),
        nbformat.v4.new_code_cell(),
        nbformat.v4.new_markdown_cell(source="**Task 11.2:**"),
        nbformat.v4.new_code_cell(),
        nbformat.v4.new_markdown_cell(source="**Task 11.3:**"),
        nbformat.v4.new_code_cell(),
    ]
    save_nb(correct_num_nb, correct_num_fn)

    # Notebook with no numbering
    no_num_fn = tmpdir.join("011-no-num.ipynb")
    no_num_nb = nbformat.v4.new_notebook()
    no_num_nb["cells"] = [
        nbformat.v4.new_markdown_cell(source="**Task:**"),
        nbformat.v4.new_code_cell(),
        nbformat.v4.new_markdown_cell(source="**Task:**"),
        nbformat.v4.new_code_cell(),
        nbformat.v4.new_markdown_cell(source="**Task:**"),
        nbformat.v4.new_code_cell(),
    ]
    save_nb(no_num_nb, no_num_fn)

    # Notebook with incorrect numbering
    incorrect_num_fn = tmpdir.join("011-incorrect-num.ipynb")
    incorrect_num_nb = nbformat.v4.new_notebook()
    incorrect_num_nb["cells"] = [
        nbformat.v4.new_markdown_cell(source="**Task 12.2:**"),
        nbformat.v4.new_code_cell(),
        nbformat.v4.new_markdown_cell(source="**Task:**"),
        nbformat.v4.new_code_cell(),
        nbformat.v4.new_markdown_cell(source="**Task 11.1:**"),
        nbformat.v4.new_code_cell(),
    ]
    save_nb(incorrect_num_nb, incorrect_num_fn)

    yield tmpdir


def test_add_task_numbers(tmpfiles):
    # Run script on fixture files
    # Scenario 1: No numbering
    add_task_numbers(tmpfiles.join("011-no-num.ipynb"))
    # Scenario 2: Incorrect numbering
    add_task_numbers(tmpfiles.join("011-incorrect-num.ipynb"))

    # Load corrected files
    correct = get_source_from_file(tmpfiles.join("011-correct-num.ipynb"))
    no_num_corrected = get_source_from_file(tmpfiles.join("011-no-num.ipynb"))
    incorrect_num_corrected = get_source_from_file(
        tmpfiles.join("011-incorrect-num.ipynb")
    )

    # Testing
    assert all(
        x == y for x, y in zip(correct, no_num_corrected)
    ), "Failed scenario 1: No numbering"
    assert all(
        x == y for x, y in zip(correct, incorrect_num_corrected)
    ), "Fail scenario 2: Incorrect numbering"
