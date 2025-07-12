from unittest.mock import patch

from nauta.cli import app, initialize_database


def test_add_accounts(runner):

    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        initialize_database()

        # Add an account
        result_add = runner.invoke(app, ["add", "test@example.com", "password123"])

        assert result_add.exit_code == 0
        assert result_add.output == "Usuario agregado: test@example.com\n"

        result_add = runner.invoke(app, ["add", "test@example.com", "password123"])

        assert result_add.exit_code == 0
        assert result_add.output == "Ya existe el usuario: test@example.com\n"


def test_delete_account(runner):
    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        initialize_database()

        runner.invoke(app, ["add", "delete@example.com", "password123"])

        result_delete = runner.invoke(app, ["delete", "delete@example.com"])

        assert result_delete.exit_code == 0
        assert "Usuario eliminado: delete@example.com\n" == result_delete.output

        result_list = runner.invoke(app, ["list"])
        assert "No hay usuarios agregados.\n" == result_list.output


def test_list_accounts(runner):

    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        initialize_database()

        result = runner.invoke(app, ["list"])

        assert result.exit_code == 0
        assert result.output == "No hay usuarios agregados.\n"


def test_add_and_list_account(runner):

    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        initialize_database()

        # Add an account
        result_add = runner.invoke(app, ["add", "test@example.com", "password123"])

        assert result_add.exit_code == 0
        assert result_add.output == "Usuario agregado: test@example.com\n"

        # List accounts
        result_list = runner.invoke(app, ["list"])

        assert result_list.exit_code == 0
        assert "test@example.com" in result_list.output


def test_set_account_default(runner):

    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        initialize_database()

        result_set_default = runner.invoke(app, ["default", "test@example.com"])

        assert result_set_default.exit_code == 0
        assert (
            result_set_default.output == "No se encontró el usuario: test@example.com\n"
        )

        # Add an account
        result_add = runner.invoke(app, ["add", "test@example.com", "password123"])

        assert result_add.exit_code == 0
        assert result_add.output == "Usuario agregado: test@example.com\n"

        result_set_default = runner.invoke(app, ["default", "test@example.com"])

        assert result_set_default.exit_code == 0

        assert (
            result_set_default.output
            == 'Usuario "test@example.com" establecido como usuario por defecto\n'
        )


def test_update_password(runner):

    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        initialize_database()

        result_update = runner.invoke(
            app, ["password", "test@example.com", "password123"]
        )

        assert result_update.exit_code == 0
        assert result_update.output == "No se encontró el usuario: test@example.com\n"

        # Add an account
        result_add = runner.invoke(app, ["add", "test@example.com", "password123"])

        assert result_add.exit_code == 0
        assert result_add.output == "Usuario agregado: test@example.com\n"

        result_update = runner.invoke(
            app, ["password", "test@example.com", "password123"]
        )

        assert result_update.exit_code == 0
        assert result_update.output == "Contraseña actualizada\n"


def test_info_password(runner):

    with patch("nauta.database.get_global_db_path", return_value="test.db"):
        initialize_database()

        result_info = runner.invoke(app, ["info", "test@example.com"])

        assert result_info.exit_code == 0
        assert result_info.output == "No se encontró el usuario: test@example.com\n"

        # Add an account
        result_add = runner.invoke(app, ["add", "test@example.com", "password123"])

        assert result_add.exit_code == 0
        assert result_add.output == "Usuario agregado: test@example.com\n"

        result_info = runner.invoke(app, ["info", "test@example.com"])

        assert result_info.exit_code == 0
        assert "👤 Información del usuario: test@example.com" in result_info.output
