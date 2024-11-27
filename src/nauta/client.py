import re
from bs4 import BeautifulSoup
import requests
from nauta.constants import HOST_URL, LOGOUT_URL, AVAILABLE_TIME_URL
from nauta.database import add_session, get_session, delete_session


class NautaClient(object):

    def __init__(self, correo, password):
        self.user = correo
        self.password = password

    def login(self):
        """Función para iniciar sesión"""

        resp = requests.get(HOST_URL, timeout=5)

        soup = BeautifulSoup(resp.text, "html.parser")

        action = soup.find("form", id="formulario")["action"]
        csrfhw = soup.find("input", {"name": "CSRFHW"})["value"]
        wlanuserip = soup.find("input", {"name": "wlanuserip"})["value"]

        resp = requests.post(
            action,
            data={
                "username": self.user,
                "password": self.password,
                "CSRFHW": csrfhw,
                "wlanuserip": wlanuserip,
            },
            headers={"content-type": "application/x-www-form-urlencoded"},
            timeout=10,
        )

        if not resp.ok:
            print("Mensaje:", resp.reason)
            return

        if not "online.do" in resp.url:
            soup = BeautifulSoup(resp.text, "html.parser")
            script_text = soup.find_all("script")[-1].get_text()
            match = re.search(r"alert\(\"(?P<reason>[^\"]*?)\"\)", script_text)
            print("Mensaje:", match and match.groupdict().get("reason"))
            return

        m = re.search(r"ATTRIBUTE_UUID=(\w+)", resp.text)

        attribute_uuid = m.group(1) if m else None

        add_session(csrfhw, self.user, wlanuserip, attribute_uuid)

    def logout(self):
        """Función para cerrar sesión"""

        session = get_session()

        resp = requests.post(
            LOGOUT_URL,
            data={
                "CSRFHW": session.csrfhw,
                "username": session.username,
                "ATTRIBUTE_UUID": session.attribute_uuid,
                "wlanuserip": session.wlanuserip,
            },
            headers={"content-type": "application/x-www-form-urlencoded"},
            timeout=10,
        )

        if not resp.ok:
            print("Mensaje:", resp.reason)
            return

        if "SUCCESS" not in resp.text.upper():
            print("Mensaje:", resp.text[:100])
            return

        delete_session()

    def available_time(self):
        """Función para obtener el tiempo disponible"""

        session = get_session()

        resp = requests.post(
            AVAILABLE_TIME_URL,
            data={
                "op": "getLeftTime",
                "ATTRIBUTE_UUID": session.attribute_uuid,
                "CSRFHW": session.csrfhw,
                "username": session.username,
            },
            headers={"content-type": "application/x-www-form-urlencoded"},
            timeout=10,
        )

        if not resp.ok:
            print("Mensaje:", resp.reason)
            return

        return resp.text
