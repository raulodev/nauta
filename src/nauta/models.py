from dataclasses import dataclass


@dataclass
class Account:
    id: int
    email: str
    password: str
    is_default: bool


@dataclass
class Session:
    id: int
    csrfhw: str
    username: str
    wlanuserip: str
    attribute_uuid: str
    created_at: int


@dataclass
class NautaClientResponse:
    error: bool
    message: str
