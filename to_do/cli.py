"""
This module is the entry point of the cli application
"""

# Libraries
from typing import Optional
from datetime import datetime
from rich.table import Table
import typer

# Local
from to_do.To_Do import ToDo
from to_do import __app_name__, __version__, SUCCESS, ERRORS, ERROR, console


app = typer.Typer()


def _version_callback(value):
    if value:
        console.print(f"{__app_name__} v{__version__}", style="info")
        raise typer.Exit(0)


def _parser_date(value):
    if value:
        try:
            date = datetime.strptime(value, "%d/%m/%Y")
            print(date)
            return date
        except ValueError as error:
            console.print(
                "Error : :loudly_crying_face: the format has to be DD/MM/YYYY",
                style="danger",
            )
            raise typer.Exit(1) from error


def _display_table(data):
    """This function display a table with the data"""
    keys = data[0].keys()
    table = Table(title="To Do")
    for key in keys:
        table.add_column(key)
    for row in data:
        table.add_row(*[str(row[key]) for key in keys])

    console.print(table)


@app.callback()
def main(
    context: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="show the cli version",
        callback=_version_callback,
        is_eager=True,
    ),
):
    """
    This function is always executed before any other command
    For this application we only want to show the version
    """
    pass


@app.command()
def init(context: typer.Context):
    """This command initialize the database"""
    todo = ToDo()
    response = todo.init_db()
    return response


@app.command()
def show():
    """This command show all to do"""
    todo = ToDo()
    data = todo.all()
    if data == []:
        console.log(
            ":sad_but_relieved_face: No Data Found :sad_but_relieved_face:",
            style="waring",
        )
    else:
        _display_table(data)


@app.command()
def search(
    query: str = typer.Argument(
        ...,
        help="search by a patter on the name",
    )
):
    """This command search a to do by a patter on the name"""
    if query == "":
        console.log("no patter to search", style="warning")
        raise typer.Exit(1)

    todo = ToDo()
    sql_query = f"name LIKE '%{query}%'"
    data = todo.filter(sql_query)
    if data == []:
        console.print(f"No To Do found with the patter {query}", style="warning")
        return SUCCESS
    else:
        _display_table(data)

    return SUCCESS


@app.command()
def create(
    name: str,
    done_by=typer.Option(
        ..., help="format DD/MM/YYYY", prompt="format DD/MM/YYYY", callback=_parser_date
    ),
):
    """This command create a new to do"""
    todo = ToDo()
    result = todo.create(name, done_by)
    if result == SUCCESS:
        todo.save()
        console.log(
            ":white_heavy_check_mark: data was successfully saved :white_heavy_check_mark:",
            style="info",
        )
    else:
        console.log(f":cross_mark: {ERRORS[result]} :cross_mark:", style="danger")
        return ERROR


@app.command()
def update(
    todo_id=typer.Argument(int),
    name=typer.Option(""),
    done_by=typer.Option("", help="format DD/MM/YYYY", callback=_parser_date),
    done=typer.Option(None),
):
    """This command update a to do"""
    todo = ToDo()
    values = {}
    if name != "":
        values["name"] = name
    if done_by:
        values["done_by"] = done_by
    if done:
        values["done"] = done

    if len(values) == 0:
        console.log("no values to be update", style="warning")
        raise typer.Exit(1)

    result = todo.update(todo_id, **values)

    if result == SUCCESS:
        todo.save()
        console.log(
            ":white_heavy_check_mark: data was successfully updated :white_heavy_check_mark:",
            style="info",
        )
    else:
        console.log(f":cross_mark: {ERRORS[result]} :cross_mark:", style="danger")
        raise typer.Exit(1)


@app.command()
def delete(todo_id):
    """This command delete a to do"""
    todo = ToDo()
    result = todo.delete(todo_id)
    if result == SUCCESS:
        todo.save()
        console.log(
            f":white_heavy_check_mark: The todo {todo_id} has been delete :white_heavy_check_mark:",
            style="info",
        )
    else:
        console.log(f":cross_mark: {ERRORS[result]} :cross_mark:", style="danger")
        raise typer.Exit(1)
