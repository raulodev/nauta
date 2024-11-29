import typer
from typing_extensions import Annotated
from nauta.database import (
    list_account,
    add_account,
    delete_account,
    update_account,
    update_password,
    get_account,
)
from nauta.secure import encrypt_password, decrypt_password, generate_key


def add(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[str, typer.Argument(help="Contraseña del usuario")],
):
    """Añade un nuevo usuario"""

    account = get_account(correo)

    if account:
        typer.echo(typer.style(f"Ya existe el usuario: {correo}", fg="yellow"))
    else:
        secure_password = encrypt_password(password, generate_key())
        add_account(correo, secure_password)
        typer.echo(typer.style(f"Usuario agregado: {correo}", fg="green"))


def delete(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Elimina un usuario"""
    account = get_account(correo)
    if account:
        delete_account(correo)
        typer.echo(typer.style(f"Usuario eliminado: {correo}", fg="green"))

        # Si queda una solo usuario registrado
        # establecerlo como usuario por defecto
        accounts = list_account()

        if len(accounts) == 1:
            update_account(accounts[0].email, True)

    else:
        typer.echo(typer.style(f"No se encontró el usuario: {correo}", fg="yellow"))


def list():  # pylint: disable=W0622
    """Lista todos los usuarios"""
    accounts = list_account()

    if accounts:
        typer.echo(
            typer.style(
                "👥 Usuarios disponibles (✅ indica usuario por defecto):", fg="cyan"
            )
        )

        for index, account in enumerate(accounts, start=1):
            is_default = "✅" if account.is_default else ""
            typer.echo(f"{index}. {account.email} {is_default}")

    else:

        typer.echo(typer.style("No hay usuarios agregados.", fg="yellow"))


def default(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Establece el usuario por defecto"""

    account = get_account(correo)
    if account:
        update_account(correo, True)
        typer.echo(
            typer.style(
                f'Usuario "{correo}" establecido como usuario por defecto', fg="green"
            )
        )

    else:
        typer.echo(typer.style(f"No se encontró el usuario: {correo}", fg="yellow"))


def password(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
    password: Annotated[  # pylint: disable=W0621
        str, typer.Argument(help="Nueva contraseña del usuario")
    ],
):
    """Establece la contraseña del usuario"""

    account = get_account(correo)
    if account:
        secure_password = encrypt_password(password, generate_key())
        update_password(correo, secure_password)
        typer.echo(typer.style("Contraseña actualizada", fg="green"))

    else:
        typer.echo(typer.style(f"No se encontró el usuario: {correo}", fg="yellow"))


def info(
    correo: Annotated[str, typer.Argument(help="Correo del usuario")],
):
    """Muestra información del usuario"""

    account = get_account(correo)
    if account:
        typer.echo(typer.style(f"👤 Información del usuario: {correo}", fg="cyan"))

        passw = decrypt_password(account.password, generate_key())
        is_default = "✅" if account.is_default else "❌"
        hidden_passw = passw[0] + (len(passw) - 1) * "*"

        typer.echo(f"- Correo: {account.email}")
        typer.echo(f"- Contraseña: {hidden_passw}")
        typer.echo(f"- Es usuario por defecto: {is_default}")
    else:
        typer.echo(typer.style(f"No se encontró el usuario: {correo}", fg="yellow"))
