# pylint: disable=redefined-builtin
import typer
from .account import add, delete, list, default, password, info
from .session import login, logout
from .database import initialize_database


initialize_database()


app = typer.Typer()
app.command()(add)
app.command()(delete)
app.command()(list)
app.command()(default)
app.command()(password)
app.command()(info)
app.command()(login)
app.command()(logout)

if __name__ == "__main__":
    app()
