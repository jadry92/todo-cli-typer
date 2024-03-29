"""This file is the entry point of the application"""

from to_do import cli, __app_name__


def main():
    """This is the main function"""
    cli.app(prog_name=__app_name__)


if __name__ == "__main__":
    main()
