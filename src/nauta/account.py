import typer
from typing_extensions import Annotated


def add(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[str, typer.Argument(help="Contraseña del usuario")],
):

    print("Añadiendo usuario")


def delete(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    print("Eliminando usuario")


def list():
    print("Listando usuarios")


def set_default(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    print("Estableciendo usuario por defecto")


def set_password(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[str, typer.Argument(help="Contraseña del usuario")],
):
    print("Estableciendo contraseña")


def info(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    print("Información del usuario")
