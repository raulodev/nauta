import sqlite3
import os
from appdirs import user_data_dir
from .models import Account

APP_NAME = "nauta"
APP_AUTHOR = "raulodev"


def get_global_db_path():
    """Directorio estándar para datos de la aplicación"""
    data_dir = user_data_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "data.db")


def initialize_database():
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Crear tabla si no existe
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

    connection.commit()
    connection.close()


def list_account() -> list[Account]:
    """Función para listar los datos de la base de datos"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Leer datos
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()

    # Mostrar datos
    return [Account(*row) for row in rows]


def add_account(email: str, password: str, is_default: bool = False) -> Account:
    """Función para agregar un nuevo elemento a la base de datos"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

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
    """Función para eliminar un elemento de la base de datos"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Eliminar datos
    cursor.execute("DELETE FROM accounts WHERE email = ?", (email,))

    connection.commit()
    connection.close()


def update_account(email: str, password: str, is_default: bool = False) -> None:
    """Función para actualizar un elemento de la base de datos"""
    db_path = get_global_db_path()
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Actualizar datos
    cursor.execute(
        """
        UPDATE accounts
        SET email = ?, password = ?, is_default = ?
        WHERE email = ?
        """,
        (email, password, is_default, email),
    )

    connection.commit()
    connection.close()
