# pylint: disable=w0622
import typer
from nauta.commands.account import add, delete, list, default, password, info
from nauta.commands.session import login, logout, time
from nauta.database import initialize_database


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
app.command()(time)

if __name__ == "__main__":
    app()
