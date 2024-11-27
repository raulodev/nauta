import sqlite3
import os
from appdirs import user_data_dir
from nauta.models import Account, Session
from nauta.constants import APP_NAME, APP_AUTHOR


def get_global_db_path():
    """Directorio estándar para datos de la aplicación"""
    data_dir = user_data_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "data.db")


def initialize_database():
    """Crear tabla si no existe"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

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

    connection.commit()
    connection.close()


def list_account() -> list[Account]:
    """Función para listar las cuentas"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Leer datos
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()

    # Mostrar datos
    return [Account(*row) for row in rows]


def get_account(email: str) -> Account:
    """Función para obtener una cuenta"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Leer datos
    cursor.execute("SELECT * FROM accounts WHERE email = ?", (email,))
    row = cursor.fetchone()

    # Mostrar datos
    return Account(*row) if row else None


def add_account(email: str, password: str, is_default: bool = True) -> None:
    """Función para agregar una nueva cuenta"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if is_default:
        accounts = list_account()
        for account in accounts:
            update_account(account.email)

    # Agregar datos
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
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Eliminar datos
    cursor.execute("DELETE FROM accounts WHERE email = ?", (email,))

    connection.commit()
    connection.close()


def update_password(email: str, password: str) -> None:
    """Función para actualizar una contraseña de usuario"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Actualizar datos
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
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    if is_default:
        accounts = list_account()
        for account in accounts:
            update_account(account.email)

    # Actualizar datos
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
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Agregar datos
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
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DELETE FROM session")

    connection.commit()
    connection.close()


def get_session():
    """Función para obtener una sesión"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Leer datos
    cursor.execute("SELECT * FROM session WHERE id = ?", (1,))
    row = cursor.fetchone()

    # Mostrar datos
    return Session(*row) if row else None
