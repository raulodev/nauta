from typing import Annotated
import typer
from nauta.client import NautaClient
from nauta.database import get_account
from nauta.secure import decrypt_password, generate_key


def login():
    """Inicia sesión en el nauta hogar"""

    account = get_account(is_default=True)

    if account:
        password = decrypt_password(account.password, generate_key())
        nauta_client = NautaClient(correo=account.email, password=password)
        nauta_client.login()

    else:
        typer.echo(typer.style("Establece un usuario por defecto", fg="yellow"))


def logout(
    force: Annotated[bool, typer.Option(help="Forzar cierre de sesión")] = False
):
    """Cierra la sesión del nauta hogar"""

    account = get_account(is_default=True)

    if account:
        password = decrypt_password(account.password, generate_key())
        nauta_client = NautaClient(correo=account.email, password=password)
        nauta_client.logout(force=force)

    else:
        typer.echo(typer.style("Establece un usuario por defecto", fg="yellow"))


def time():
    """Muestra el tiempo disponible"""

    account = get_account(is_default=True)

    if account:
        password = decrypt_password(account.password, generate_key())
        nauta_client = NautaClient(correo=account.email, password=password)
        available_time = nauta_client.available_time()

        if available_time:

            typer.echo(
                typer.style(
                    f"Tiempo disponible: {available_time}", fg="cyan", bold=True
                )
            )

    else:
        typer.echo(typer.style("Establece un usuario por defecto", fg="yellow"))
