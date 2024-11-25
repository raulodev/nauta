import typer
from typing_extensions import Annotated
from .database import list_account


def add(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[str, typer.Argument(help="Contraseña del usuario")],
):
    """Añade un nuevo usuario"""

    print("Añadiendo usuario")


def delete(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Elimina un usuario"""
    print("Eliminando usuario")


def list():
    """Lista todos los usuarios"""
    list_account()
    print("Listando usuarios")


def default(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Establece el usuario por defecto"""

    print("Estableciendo usuario por defecto")


def password(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[str, typer.Argument(help="Contraseña del usuario")],
):
    """Establece la contraseña del usuario"""
    print("Estableciendo contraseña")


def info(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Muestra información del usuario"""
    print("Información del usuario")
