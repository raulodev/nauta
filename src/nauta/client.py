import requests
from .constants import HOST_URL, LOGOUT_URL, LOGIN_URL


# TODO : iniciar sesion , cerrar sesion y obtener hora y hora restantes
class NautaClient(object):

    def __init__(self, correo, password):
        self.user = correo
        self.password = password
        self.session = None
