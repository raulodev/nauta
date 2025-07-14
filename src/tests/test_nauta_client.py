from unittest.mock import MagicMock, patch

# pylint: disable=W0622
from requests import ConnectionError


@patch("nauta.client.requests.get")
@patch("nauta.client.requests.post")
@patch("nauta.client.add_session")
def test_login_success(mock_add_session, mock_requests_post, mock_requests_get, client):

    response_get = MagicMock()
    response_get.text = """
        <form id="formulario" action="https://login.nauta.cu">
            <input name="CSRFHW" value="csrf-token">
            <input name="wlanuserip" value="192.168.1.1">
        </form>
    """

    mock_requests_get.return_value = response_get

    response_post = MagicMock()
    response_post.text = "ATTRIBUTE_UUID=abc123"
    response_post.ok = True
    response_post.url = "online.do"

    mock_requests_post.return_value = response_post

    response = client.login()

    mock_add_session.assert_called_once_with(
        "csrf-token", "correo@nauta.com.cu", "192.168.1.1", "abc123"
    )

    assert response.message == "Sesión iniciada"
    assert not response.error


@patch("nauta.client.requests.get")
def test_login_connection_error(mock_requests_get, client):

    mock_requests_get.side_effect = ConnectionError()

    response = client.login()

    assert response.message == "No se pudo conectar con el servidor"
    assert response.error


@patch("nauta.client.requests.get")
@patch("nauta.client.requests.post")
def test_login_not_resp_ok(mock_requests_post, mock_requests_get, client):

    response_get = MagicMock()
    response_get.text = """
        <form id="formulario" action="https://login.nauta.cu">
            <input name="CSRFHW" value="csrf-token">
            <input name="wlanuserip" value="192.168.1.1">
        </form>
    """

    mock_requests_get.return_value = response_get

    response_post = MagicMock()
    response_post.text = "ATTRIBUTE_UUID=abc123"
    response_post.ok = False
    response_post.reason = "Error de autenticación"

    mock_requests_post.return_value = response_post

    response = client.login()

    assert response.message == "Error de autenticación"
    assert response.error


@patch("nauta.client.requests.post")
@patch("nauta.client.delete_session")
def test_logout_success(mock_delete, mock_post, client):

    session = MagicMock()
    session.csrfhw = "csrf"
    session.username = "correo@nauta.com.cu"
    session.attribute_uuid = "abc123"
    session.wlanuserip = "192.168.1.1"

    mock_post.return_value.ok = True
    mock_post.return_value.text = "SUCCESS"

    response = client.logout(session)

    assert response.message == "Sesión cerrada"
    assert not response.error

    response = client.logout(session, force=True)

    assert response.message == "Sesión eliminada"
    assert not response.error

    mock_delete.assert_called()


@patch("nauta.client.requests.post")
def test_logout_connection_error(mock_post, client):

    session = MagicMock()
    session.csrfhw = "csrf"
    session.username = "correo@nauta.com.cu"
    session.attribute_uuid = "abc123"
    session.wlanuserip = "192.168.1.1"

    mock_post.side_effect = ConnectionError()

    response = client.logout(session)

    assert response.message == "No se pudo conectar con el servidor"
    assert response.error


@patch("nauta.client.requests.post")
def test_logout_not_resp_ok(mock_post, client):

    session = MagicMock()
    session.csrfhw = "csrf"
    session.username = "correo@nauta.com.cu"
    session.attribute_uuid = "abc123"
    session.wlanuserip = "192.168.1.1"

    mock_post.return_value.ok = False
    mock_post.return_value.reason = "Error"

    response = client.logout(session)

    assert response.message == "Error"
    assert response.error


@patch("nauta.client.requests.post")
def test_available_time_success(mock_post, client):

    session = MagicMock()
    session.csrfhw = "csrf"
    session.username = "correo@nauta.com.cu"
    session.attribute_uuid = "abc123"

    mock_post.return_value.ok = True
    mock_post.return_value.text = "30 minutos"

    response = client.available_time(session)

    assert response.message == "30 minutos"
    assert not response.error
