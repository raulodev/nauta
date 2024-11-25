import typer
from typing_extensions import Annotated
from .database import (
    list_account,
    add_account,
    delete_account,
    update_account,
    update_password,
    get_account,
)
from .secure import encrypt_password, decrypt_password, generate_key


def add(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[str, typer.Argument(help="Contraseña del usuario")],
):
    """Añade un nuevo usuario"""

    secure_password = encrypt_password(password, generate_key())
    add_account(correo, secure_password)
    typer.echo("Usuario añadido ✅")


def delete(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Elimina un usuario"""
    account = get_account(correo)
    if account:
        delete_account(correo)
        typer.echo("Usuario eliminado ✅")
    else:
        typer.echo("No se encontró la cuenta")


def list():  # pylint: disable=redefined-builtin
    """Lista todos los usuarios"""
    accounts = list_account()

    if accounts:
        typer.echo("👥 Usuarios disponibles:")
        for index, account in enumerate(accounts, start=1):
            is_default = "✅" if account.is_default else ""
            typer.echo(f"{index}. {account.email} {is_default}")

    else:
        typer.echo("No se encontraron usuarios")


def default(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Establece el usuario por defecto"""

    account = get_account(correo)
    if account:
        update_account(correo, True)
        typer.echo(f"Usuario {correo} establecido como default ✅")
    else:
        typer.echo("No se encontró la cuenta")


def password(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[str, typer.Argument(help="Nueva contraseña del usuario")],
):
    """Establece la contraseña del usuario"""

    account = get_account(correo)
    if account:
        secure_password = encrypt_password(password, generate_key())
        update_password(correo, secure_password)
        typer.echo("Contraseña actualizada ✅")
    else:
        typer.echo("No se encontró la cuenta")


def info(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Muestra información del usuario"""

    account = get_account(correo)
    if account:
        typer.echo("👤 Información del usuario:")
        passw = decrypt_password(account.password, generate_key())
        is_default = "✅" if account.is_default else "❌"
        typer.echo(f"Correo: {account.email}")
        typer.echo(f"Contraseña: {passw}")
        typer.echo(f"Es default: {is_default}")
    else:
        typer.echo("No se encontró la cuenta")
