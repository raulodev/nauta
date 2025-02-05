import re

import requests
import typer
from bs4 import BeautifulSoup
from requests import ConnectionError, ReadTimeout

from nauta.constants import AVAILABLE_TIME_URL, HOST_URL, LOGOUT_URL
from nauta.database import add_session, delete_session, get_session


class NautaClient(object):

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    def __init__(self, correo, password):
        self.correo = correo
        self.password = password

    def login(self):
        """Función para iniciar sesión"""

        try:
            session = get_session()

            if session:
                typer.echo(
                    typer.style(
                        'Cierre la sesión actual con el comando: "nauta logout"',
                        fg="yellow",
                        bold=True,
                    )
                )
                return

            resp = requests.get(HOST_URL, timeout=60)

            soup = BeautifulSoup(resp.text, "html.parser")

            action = soup.find("form", id="formulario")["action"]
            csrfhw = soup.find("input", {"name": "CSRFHW"})["value"]
            wlanuserip = soup.find("input", {"name": "wlanuserip"})["value"]

            resp = requests.post(
                action,
                data={
                    "username": self.correo,
                    "password": self.password,
                    "CSRFHW": csrfhw,
                    "wlanuserip": wlanuserip,
                },
                headers=self.headers,
                timeout=60,
            )

            if not resp.ok:
                typer.echo(typer.style(resp.reason, fg="red", bold=True))
                return

            if not "online.do" in resp.url:
                soup = BeautifulSoup(resp.text, "html.parser")
                script_text = soup.find_all("script")[-1].get_text()
                match = re.search(r"alert\(\"(?P<reason>[^\"]*?)\"\)", script_text)
                typer.echo(
                    typer.style(
                        match and match.groupdict().get("reason"), fg="red", bold=True
                    )
                )
                return

            m = re.search(r"ATTRIBUTE_UUID=(\w+)", resp.text)

            attribute_uuid = m.group(1) if m else None

            add_session(csrfhw, self.correo, wlanuserip, attribute_uuid)

            typer.echo(
                typer.style(
                    ("Sesión iniciada"),
                    fg="green",
                    bold=True,
                ),
                nl=False,
            )
            available_time = self.available_time()

            if available_time:

                typer.echo(
                    message=typer.style(
                        f": {available_time} tiempo disponible", bold=True
                    ),
                )

        except (ConnectionError, ReadTimeout):
            typer.echo(
                typer.style(
                    ("No se pudo conectar con el servidor"), fg="red", bold=True
                )
            )

    def logout(self, force=False):
        """Función para cerrar sesión"""

        try:
            session = get_session()

            if not session:
                typer.echo(
                    typer.style(
                        'Primero inicie sesión con el comando: "nauta login"',
                        fg="yellow",
                        bold=True,
                    )
                )
                return

            available_time = None

            if not force:

                available_time = self.available_time()

                resp = requests.post(
                    LOGOUT_URL,
                    data={
                        "CSRFHW": session.csrfhw,
                        "username": session.username,
                        "ATTRIBUTE_UUID": session.attribute_uuid,
                        "wlanuserip": session.wlanuserip,
                    },
                    headers=self.headers,
                    timeout=60,
                )

                if not resp.ok:
                    typer.echo(typer.style(resp.reason, fg="red", bold=True))
                    return

                if "FAILURE" in resp.text.upper() and not force:
                    typer.echo(
                        typer.style("No se pudo cerrar la sesión", fg="red", bold=True)
                    )
                    return

                if "SUCCESS" not in resp.text.upper() and not force:
                    typer.echo(typer.style(resp.text[:100], fg="red", bold=True))
                    return

            delete_session()

            typer.echo(
                typer.style(
                    ("Sesión cerrada" if not force else "Sesión eliminada"),
                    fg="green",
                    bold=True,
                ),
                nl=force,
            )

            if available_time:

                typer.echo(
                    message=typer.style(
                        f": {available_time} tiempo disponible para la próxima conexión",
                        bold=True,
                    ),
                )

        except (ConnectionError, ReadTimeout):
            typer.echo(
                typer.style(
                    ("No se pudo conectar con el servidor"), fg="red", bold=True
                )
            )

    def available_time(self) -> str:
        """Función para obtener el tiempo disponible"""

        try:

            session = get_session()

            if not session:
                typer.echo(
                    typer.style(
                        'Primero inicie sesión con el comando: "nauta login"',
                        fg="yellow",
                        bold=True,
                    )
                )
                return

            resp = requests.post(
                AVAILABLE_TIME_URL,
                data={
                    "op": "getLeftTime",
                    "ATTRIBUTE_UUID": session.attribute_uuid,
                    "CSRFHW": session.csrfhw,
                    "username": session.username,
                },
                headers=self.headers,
                timeout=60,
            )

            if not resp.ok or "error" in resp.text:
                raise ConnectionError

            return resp.text

        except (ConnectionError, ReadTimeout):
            typer.echo(
                typer.style(("No se pudo obtener el tiempo"), fg="red", bold=True)
            )
