from fastapi.testclient import TestClient
from src.app import activities


def test_root_redirect(client: TestClient):
    # Arrange: client fixture provided

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    # URL is a starlette URL object; convert to str or check the path
    assert str(response.url).endswith("/static/index.html")


def test_get_activities(client: TestClient):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == activities


def test_signup_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in activities[activity]["participants"]


def test_signup_activity_not_found(client: TestClient):
    # Arrange
    activity = "Nonexistent"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_signed(client: TestClient):
    # Arrange
    activity = "Chess Club"
    existing = activities[activity]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": existing})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = activities[activity]["participants"][0]

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}
    assert email not in activities[activity]["participants"]


def test_unregister_activity_not_found(client: TestClient):
    # Arrange
    activity = "Nonexistent"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_not_signed(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "nobody@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"
