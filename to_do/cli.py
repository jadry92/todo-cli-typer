# Libraries
import typer
from typing import Optional
from rich.console import Console
from rich.style import Style
from rich.theme import Theme
from datetime import datetime
from rich.table import Table
# Local
from to_do.To_Do import ToDo
from to_do.db import Database
from to_do import __app_name__, __version__, SUCCESS, ERRORS, ERROR

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})

console = Console(theme=custom_theme)
app = typer.Typer()


def _version_callback(value):
    if value:
        console.print(f"{__app_name__} v{__version__}f")
        raise typer.Exit(0)


def _parser_date(value):
    if value:
        try:
            date = datetime.strptime(value, "%d/%m/%Y")
            print(date)
            return date
        except ValueError:
            console.log(
                ":loudly_crying_face: the format has to be DD/MM/YYYY", style="danger")
            raise typer.Exit(1)


@app.callback()
def main(
    context: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="show the cli version",
        callback=_version_callback,
        is_eager=True
    )
):
    context.obj = Database()


@app.command()
def init(context: typer.Context):
    todo = ToDo()
    response = todo.init_db()
    return response


@app.command()
def show():
    todo = ToDo()
    data = todo.all()
    if data == []:
        console.log(
            f":sad_but_relieved_face: No Data Found :sad_but_relieved_face:", style="waring")
    keys = data[0].keys()
    table = Table(title="To Do")
    for key in keys:
        table.add_column(key)
    for row in data:
        table.add_row(*[str(row[key]) for key in keys])
    console.print(table)


@app.command()
def create(
    name: str,
    done_by=typer.Option(...,
                         help="format DD/MM/YYYY", prompt="format DD/MM/YYYY", callback=_parser_date)
):
    todo = ToDo()
    result = todo.create(name, done_by)
    if result == SUCCESS:
        todo.save()
        console.log(
            ":white_heavy_check_mark: data was successfully saved :white_heavy_check_mark:", style="info")
    else:
        console.log(
            f":cross_mark: {ERRORS[result]} :cross_mark:", style="danger")
        return ERROR


@app.command()
def update(todo_id=typer.Argument(int),
           name=typer.Option(''),
           done_by=typer.Option('',
                                help="format DD/MM/YYYY",
                                callback=_parser_date),
           done=typer.Option(None)):
    todo = ToDo()
    values = {}
    if name != '':
        values['name'] = name
    if done_by:
        values['done_by'] = done_by
    if done:
        values['done'] = done

    if not len(values):
        console.log("no values to be update", style="warning")
        raise typer.Exit(1)

    result = todo.update(todo_id, **values)

    if result == SUCCESS:
        todo.save()
        console.log(
            ":white_heavy_check_mark: data was successfully updated :white_heavy_check_mark:", style="info")
    else:
        console.log(
            f":cross_mark: {ERRORS[result]} :cross_mark:", style="danger")
        return ERROR


@app.command()
def delete(todo_id):
    todo = ToDo()
    result = todo.delete(todo_id)
    if result == SUCCESS:
        todo.save()
        console.log(
            f":white_heavy_check_mark: The todo {todo_id} has been delete :white_heavy_check_mark:", style="info")
    else:
        console.log(
            f":cross_mark: {ERRORS[result]} :cross_mark:", style="danger")
        return ERROR
