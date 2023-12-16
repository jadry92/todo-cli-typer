from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"info": "dim cyan", "warning": "magenta", "danger": "bold red"})

console = Console(theme=custom_theme)


__version__ = 1.0
__app_name__ = "to_do"

(SUCCESS, ERROR, DB_ERROR, DATA_ERROR) = range(4)

ERRORS = {
    ERROR: "General Error",
    DB_ERROR: "Database Error",
    DATA_ERROR: "The data introduce is incorrect",
}
