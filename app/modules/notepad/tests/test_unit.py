import pytest
from unittest.mock import MagicMock, patch
from app.modules.conftest import login, logout
from app.modules.auth.models import User
from app import db


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Crear usuario de prueba para los tests
        user = User.query.filter_by(email='user@example.com').first()
        if not user:
            user = User(email='user@example.com')
            user.set_password('test1234')
            db.session.add(user)
            db.session.commit()

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"

# Tests básicos para el modelo Notepad
def test_notepad_model_creation():
    """Test de creación básica del modelo Notepad"""
    from app.modules.notepad.models import Notepad
    
    notepad = Notepad(
        title="Test Note",
        body="This is a test note"
    )
    assert notepad.title == "Test Note"
    assert notepad.body == "This is a test note"

# Tests para validaciones del modelo
def test_notepad_empty_title():
    """Test para verificar comportamiento con título vacío"""
    from app.modules.notepad.models import Notepad
    
    notepad = Notepad(title="", body="Body")
    # El modelo debería aceptar o rechazar títulos vacíos según la lógica implementada
    assert notepad.title == "" or notepad.title is None


def test_notepad_empty_body():
    """Test para verificar comportamiento con cuerpo vacío"""
    from app.modules.notepad.models import Notepad
    
    notepad = Notepad(title="Title", body="")
    assert notepad.body == "" or notepad.body is None


# Tests para el servicio de Notepad
@patch('app.modules.notepad.services.NotepadRepository')
def test_notepad_service_exists(mock_repository):
    """Test para verificar que el servicio existe y puede ser instanciado"""
    from app.modules.notepad.services import NotepadService
    
    service = NotepadService()
    assert service is not None


# Tests para el repositorio de Notepad
def test_notepad_repository_exists():
    """Test para verificar que el repositorio existe y puede ser instanciado"""
    from app.modules.notepad.repositories import NotepadRepository
    
    repository = NotepadRepository()
    assert repository is not None

def test_list_empty_notepad_get(test_client):
    """
    Tests access to the empty notepad list via GET request
    """
    login_response = login(test_client, 'user@example.com', 'test1234')
    assert login_response.status_code == 200, "Login failed during test setup"

    response = test_client.get('/notepad')
    assert response.status_code == 200, "The notepad page could not be accessed"
    assert b"You have no notepads" in response.data, "Notepad content not found in response"

    logout(test_client)



