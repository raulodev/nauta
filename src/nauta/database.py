import os
import secrets
import sqlite3
from typing import List

from appdirs import user_data_dir

from nauta.constants import APP_AUTHOR, APP_NAME
from nauta.models import Account, Session


def get_global_db_path():
    """Directorio estándar para datos de la aplicación"""
    data_dir = user_data_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "data.db")


def create_conn():

    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    return connection, connection.cursor()


def clear_database():
    """Función para limpiar la base de datos para fines de testing"""

    connection, cursor = create_conn()
    cursor.execute("DROP TABLE IF EXISTS accounts")
    cursor.execute("DROP TABLE IF EXISTS session")
    cursor.execute("DROP TABLE IF EXISTS secret")

    connection.commit()
    connection.close()


def initialize_database():
    """Crear tabla si no existe"""

    connection, cursor = create_conn()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            is_default INTEGER NOT NULL
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS session (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            csrfhw TEXT NOT NULL,
            username TEXT NOT NULL,
            wlanuserip TEXT NOT NULL,
            attribute_uuid TEXT NOT NULL,
            created_at REAL DEFAULT (CAST(strftime('%f', 'now') AS REAL))
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS secret (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            data TEXT NOT NULL
        )
    """
    )

    secret = get_secret()
    if not secret:
        create_secret()

    connection.commit()
    connection.close()


def create_secret():
    """Función para crear la clave secreta"""

    connection, cursor = create_conn()

    secret = secrets.token_hex(16)
    cursor.execute(
        "INSERT INTO secret (data) VALUES (?)",
        (secret,),
    )

    connection.commit()
    connection.close()


def get_secret():
    """Función para obtener la clave secreta"""

    _, cursor = create_conn()

    row = cursor.execute("SELECT data FROM secret").fetchone()

    return row[0] if row else None


def list_account() -> List[Account]:
    """Función para listar las cuentas"""
    _, cursor = create_conn()

    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()

    return [Account(*row) for row in rows]


def get_account(email: str = None, is_default: bool = None) -> Account:
    """Función para obtener una cuenta"""
    _, cursor = create_conn()

    if email:

        cursor.execute("SELECT * FROM accounts WHERE email = ?", (email,))

    if is_default:

        cursor.execute("SELECT * FROM accounts WHERE is_default = 1")

    row = cursor.fetchone()

    return Account(*row) if row else None


def add_account(email: str, password: str, is_default: bool = True) -> None:
    """Función para agregar una nueva cuenta"""

    connection, cursor = create_conn()

    if is_default:
        accounts = list_account()
        for account in accounts:
            update_account(account.email)

    cursor.execute(
        """
        INSERT INTO accounts (email, password, is_default)
        VALUES (?, ?, ?)
        """,
        (email, password, is_default),
    )

    connection.commit()
    connection.close()


def delete_account(email: str) -> None:
    """Función para eliminar una cuenta"""
    connection, cursor = create_conn()

    cursor.execute("DELETE FROM accounts WHERE email = ?", (email,))

    connection.commit()
    connection.close()


def update_password(email: str, password: str) -> None:
    """Función para actualizar una contraseña de usuario"""

    connection, cursor = create_conn()

    cursor.execute(
        """
        UPDATE accounts
        SET password = ?
        WHERE email = ?
        """,
        (password, email),
    )

    connection.commit()
    connection.close()


def update_account(email: str, is_default: bool = False) -> None:
    """Función para actualizar una cuenta"""

    connection, cursor = create_conn()

    if is_default:
        accounts = list_account()
        for account in accounts:
            update_account(account.email)

    cursor.execute(
        """
        UPDATE accounts
        SET email = ?, is_default = ?
        WHERE email = ?
        """,
        (email, is_default, email),
    )

    connection.commit()
    connection.close()


def add_session(
    csrfhw: str, username: str, wlanuserip: str, attribute_uuid: str
) -> None:
    """Función para agregar una nueva sesión"""

    connection, cursor = create_conn()

    cursor.execute(
        """
        INSERT INTO session (csrfhw, username, wlanuserip, attribute_uuid)
        VALUES (?, ?, ?, ?)
        """,
        (csrfhw, username, wlanuserip, attribute_uuid),
    )

    connection.commit()
    connection.close()


def delete_session() -> None:
    """Función para eliminar una sesión"""

    connection, cursor = create_conn()

    cursor.execute("DELETE FROM session")

    connection.commit()
    connection.close()


def get_session():
    """Función para obtener una sesión"""

    _, cursor = create_conn()

    cursor.execute("SELECT * FROM session WHERE id = 1")
    row = cursor.fetchone()

    return Session(*row) if row else None
