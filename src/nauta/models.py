from dataclasses import dataclass


@dataclass
class Account:
    id: int
    email: str
    password: str
    is_default: bool
