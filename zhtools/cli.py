from typer import Typer

from zhtools.commands import version

app = Typer(no_args_is_help=True)

app.add_typer(version.app)


if __name__ == '__main__':
    app()
