# pylint: disable=redefined-builtin
import typer
from .account import add, delete, list, set_default, set_password, info
from .session import login, logout


app = typer.Typer()
app.command()(add)
app.command()(delete)
app.command()(list)
app.command()(set_default)
app.command()(set_password)
app.command()(info)
app.command()(login)
app.command()(logout)

if __name__ == "__main__":
    app()
