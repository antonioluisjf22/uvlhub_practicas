import pytest
from app.modules.conftest import login, logout
from app import db
from app.modules.auth.models import User
from app.modules.profile.models import UserProfile

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.

        user_test = User(email="user@example.com", password="test1234")
        db.session.add(user_test)
        db.session.commit()

        profile = UserProfile(user_id=user_test.id, name="Name", surname="Surname")
        db.session.add(profile)
        db.session.commit()
        pass

    yield test_client


def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"


def test_list_empty_notepad_get(test_client):
    """
    Tests access to the empty notepad list via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"You have no notepads." in response.data, "The expected content is not present on the page"

    logout(test_client)

def test_show_notepad(test_client):
    """
    Tests access to a specific notepad via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    # First, create a notepad to show
    response = test_client.post("/notepad/create", data={
        "title": "Test Notepad",
        "body": "This is a test notepad body."
    }, follow_redirects=True)
    assert response.status_code == 200, "Notepad creation failed."

    # Now, try to access the created notepad
    response = test_client.get(f"/notepad/1")
    assert response.status_code == 200, "Notepad could not be accessed."
    assert b"Test Notepad" in response.data, "Notepad title is not present."
    assert b"This is a test notepad body." in response.data, "Notepad body is not present."

    logout(test_client)

def test_create_notepad(test_client):
    """
    Tests the creation of a new notepad via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    response = test_client.post("/notepad/create", data={
        "title": "New Notepad",
        "body": "Content of the new notepad."
    }, follow_redirects=True)
    assert response.status_code == 200, "Notepad creation failed."
    assert b"New Notepad" in response.data, "Notepad title is not present after creation."
    assert b"Content of the new notepad." in response.data, "Notepad body is not present after creation."   

    logout(test_client)

def test_edit_notepad(test_client):
    """
    Tests editing an existing notepad via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    # First, create a notepad to edit
    response = test_client.post("/notepad/create", data={
        "title": "Editable Notepad",
        "body": "This notepad will be edited."
    }, follow_redirects=True)
    assert response.status_code == 200, "Notepad creation failed."

    # Now, edit the notepad
    response = test_client.post("/notepad/edit/1", data={
        "title": "Edited Notepad",
        "body": "This notepad has been edited."
    }, follow_redirects=True)
    assert response.status_code == 200, "Notepad editing failed."

    # Verify the changes
    response = test_client.get("/notepad/1")
    assert b"Edited Notepad" in response.data, "Notepad title was not updated."
    assert b"This notepad has been edited." in response.data, "Notepad body was not updated."

    logout(test_client)

def test_delete_notepad(test_client):
    """
    Tests deleting an existing notepad via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."
    # First, create a notepad to delete
    response = test_client.post("/notepad/create", data={
        "title": "Deletable Notepad",
        "body": "This notepad will be deleted."
    }, follow_redirects=True)
    assert response.status_code == 200, "Notepad creation failed."

    # Now, delete the notepad
    response = test_client.post("/notepad/delete/1", follow_redirects=True)
    assert response.status_code == 200, "Notepad deletion failed."

    # Verify the notepad is no longer accessible
    response = test_client.get("/notepad/1")
    assert response.status_code == 404, "Notepad was not deleted successfully."

    logout(test_client)


