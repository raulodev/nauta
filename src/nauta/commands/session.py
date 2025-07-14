from typing import Annotated

import typer

# pylint: disable=E0401
from nauta.client import NautaClient
from nauta.database import get_account, get_session
from nauta.secure import decrypt_password, generate_key


def login(
    correo: Annotated[
        str, typer.Argument(help="Correo del usuario", show_default=False)
    ] = None,
):
    """Inicia sesión en el nauta hogar. Si no se especifica un correo, se usará el usuario por defecto."""

    session = get_session()

    if session:
        typer.echo(
            typer.style(
                "Primero cierre la sesión actual con el comando: 'nauta logout'",
                fg="yellow",
            )
        )
        return

    account = get_account(is_default=True)

    if correo:
        account = get_account(correo)

    if account:
        password = decrypt_password(account.password, generate_key())
        nauta_client = NautaClient(correo=account.email, password=password)
        response = nauta_client.login()

        if response.error:
            typer.echo(typer.style(response.message, fg="red"))

        else:
            time_response = nauta_client.available_time(get_session())

            typer.echo(typer.style(response.message, fg="green"))

            if not time_response.error:
                typer.echo(
                    typer.style(
                        f"Tiempo disponible: {time_response.message}",
                    )
                )

    elif correo:
        typer.echo(
            typer.style(
                f"No se encontró el usuario: {correo}",
                fg="yellow",
            )
        )

    else:
        typer.echo(
            typer.style(
                "Establece un usuario por defecto",
                fg="yellow",
            )
        )


def logout(
    force: Annotated[
        bool,
        typer.Option("--force/--no-force", "-f/-F", help="Eliminar la sesión"),
    ] = False,
):
    """Cierra la sesión del nauta hogar"""

    session = get_session()

    if not session:
        typer.echo(
            typer.style(
                "Primero inicie sesión con el comando: 'nauta login'",
                fg="yellow",
            )
        )
        return

    nauta_client = NautaClient()

    time_response = nauta_client.available_time(session)

    response = nauta_client.logout(session, force=force)

    if response.error:
        typer.echo(typer.style(response.message, fg="red"))
        typer.echo(
            typer.style(
                "Intente usar el comando 'nauta logout -f' si la sesión ya está cerrada."
            )
        )
    else:
        typer.echo(typer.style(response.message, fg="green"))

        if not time_response.error:
            typer.echo(
                typer.style(
                    f"Tiempo disponible para la próxima conexión: {time_response.message}",
                )
            )


def time():
    """Muestra el tiempo disponible"""

    session = get_session()

    if not session:
        typer.echo(
            typer.style(
                "Primero inicie sesión con el comando: 'nauta login'",
                fg="yellow",
            )
        )
        return

    nauta_client = NautaClient()
    response = nauta_client.available_time(session)

    if response.error:
        typer.echo(typer.style(response.message, fg="red"))
    else:
        typer.echo(typer.style(f"Tiempo disponible: {response.message}"))
