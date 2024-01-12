# Library
import pytest
from datetime import datetime, timedelta
from typer.testing import CliRunner

# local
from to_do.cli import __app_name__, __version__, app
from to_do.To_Do import ToDo


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def todo():
    return ToDo()


def test_create_command(runner, todo):
    done_by_date = datetime.now() + timedelta(days=2)
    done_by_date_str = done_by_date.strftime("%d/%m/%Y")
    result = runner.invoke(
        app, ["create", "Buy groceries", "--done-by", done_by_date_str]
    )
    assert "data was successfully saved" in result.stdout


def test_show_command(runner):
    result = runner.invoke(app, ["show"])
    assert result.exit_code == 0
    assert "To Do" in result.stdout


def test_delete_command(runner, todo):
    all_todo = todo.all()
    todo_id = all_todo[0]["id"]
    result = runner.invoke(app, ["delete", f"{todo_id}"])
    assert f"has been delete" in result.stdout


def test_update_command(runner, todo):
    all_todo = todo.all()
    todo_id = all_todo[0]["id"]
    result = runner.invoke(
        app,
        ["update", f"{todo_id}", "--name", "buy new things", "--done-by", "20/03/2023"],
    )
    assert f"data was successfully updated" in result.stdout


def test_search_command(runner, todo):
    # First, create some to-do items for the test
    runner.invoke(app, ["create", "Buy groceries", "--done-by", "20/02/2023"])
    runner.invoke(app, ["create", "Buy medicine", "--done-by", "21/02/2023"])

    # Now, search for a to-do item
    result = runner.invoke(app, ["search", "groceries"])
    assert result.exit_code == 0
    assert "Buy groceries" in result.stdout
    assert "Buy medicine" not in result.stdout
