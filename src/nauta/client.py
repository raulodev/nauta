import re

import requests
from bs4 import BeautifulSoup

# pylint: disable=W0622
from requests import ConnectionError, ReadTimeout

from nauta.constants import AVAILABLE_TIME_URL, HOST_URL, LOGOUT_URL
from nauta.database import add_session, delete_session
from nauta.models import NautaClientResponse, Session


class NautaClient:

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    def __init__(self, correo: str = None, password: str = None):
        self.correo = correo
        self.password = password

    def login(self):
        """Función para iniciar sesión"""

        try:

            resp = requests.get(HOST_URL, timeout=30)

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
                timeout=30,
            )

            if not resp.ok:
                return NautaClientResponse(error=True, message=resp.reason)

            if not "online.do" in resp.url:
                soup = BeautifulSoup(resp.text, "html.parser")
                script_text = soup.find_all("script")[-1].get_text()
                match = re.search(r"alert\(\"(?P<reason>[^\"]*?)\"\)", script_text)
                return NautaClientResponse(
                    error=True, message=match and match.groupdict().get("reason")
                )

            m = re.search(r"ATTRIBUTE_UUID=(\w+)", resp.text)

            attribute_uuid = m.group(1) if m else None

            add_session(csrfhw, self.correo, wlanuserip, attribute_uuid)

            return NautaClientResponse(error=False, message="Sesión iniciada")

        except (ConnectionError, ReadTimeout):
            return NautaClientResponse(
                error=True, message="No se pudo conectar con el servidor"
            )

    def logout(self, session: Session, force=False):
        """Función para cerrar sesión"""

        try:

            if not force:

                resp = requests.post(
                    LOGOUT_URL,
                    data={
                        "CSRFHW": session.csrfhw,
                        "username": session.username,
                        "ATTRIBUTE_UUID": session.attribute_uuid,
                        "wlanuserip": session.wlanuserip,
                    },
                    headers=self.headers,
                    timeout=30,
                )

                if not resp.ok:
                    return NautaClientResponse(error=True, message=resp.reason)

                if "FAILURE" in resp.text.upper() and not force:
                    return NautaClientResponse(
                        error=True, message="No se pudo cerrar la sesión"
                    )

                if "SUCCESS" not in resp.text.upper() and not force:
                    return NautaClientResponse(error=True, message=resp.text[:100])

            delete_session()

            return NautaClientResponse(
                error=False,
                message="Sesión cerrada" if not force else "Sesión eliminada",
            )

        except (ConnectionError, ReadTimeout):
            return NautaClientResponse(
                error=True, message="No se pudo conectar con el servidor"
            )

    def available_time(self, session: Session):
        """Función para obtener el tiempo disponible"""

        try:

            if not session:
                return NautaClientResponse(
                    error=True,
                    message="Primero inicie sesión con el comando: 'nauta login'",
                )

            resp = requests.post(
                AVAILABLE_TIME_URL,
                data={
                    "op": "getLeftTime",
                    "ATTRIBUTE_UUID": session.attribute_uuid,
                    "CSRFHW": session.csrfhw,
                    "username": session.username,
                },
                headers=self.headers,
                timeout=30,
            )

            if not resp.ok or "error" in resp.text:
                raise ConnectionError

            return NautaClientResponse(error=False, message=resp.text)

        except (ConnectionError, ReadTimeout):
            return NautaClientResponse(
                error=True, message="No se pudo obtener el tiempo disponible"
            )
