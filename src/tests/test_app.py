from src.app import activities


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

def test_get_activities_returns_200(client):
    # Arrange — client fixture provides a clean state

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_dict(client):
    # Arrange — client fixture pre-populates "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_success(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()


def test_signup_adds_participant(client):
    # Arrange
    email = "new@mergington.edu"

    # Act
    client.post("/activities/Chess Club/signup", params={"email": email})
    response = client.get("/activities")

    # Assert
    participants = response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_duplicate_rejected(client):
    # Arrange — "michael@mergington.edu" is already in the fixture state

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_unknown_activity_rejected(client):
    # Arrange
    unknown_activity = "Underwater Basket Weaving"

    # Act
    response = client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": "new@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404


def test_signup_activity_full_rejected(client):
    # Arrange — fixture sets max_participants=2; one spot is already taken;
    # fill the last remaining spot first
    client.post("/activities/Chess Club/signup", params={"email": "fill@mergington.edu"})

    # Act — try to add one more beyond the limit
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "overflow@mergington.edu"},
    )

    # Assert
    assert response.status_code == 400
    assert "full" in response.json()["detail"]


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/participants
# ---------------------------------------------------------------------------

def test_unregister_success(client):
    # Arrange — "michael@mergington.edu" exists in the fixture state

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 200
    assert "message" in response.json()


def test_unregister_removes_participant(client):
    # Arrange — "michael@mergington.edu" exists in the fixture state

    # Act
    client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )
    response = client.get("/activities")

    # Assert
    participants = response.json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants


def test_unregister_unknown_participant_rejected(client):
    # Arrange
    unknown_email = "ghost@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": unknown_email},
    )

    # Assert
    assert response.status_code == 404


def test_unregister_unknown_activity_rejected(client):
    # Arrange
    unknown_activity = "Underwater Basket Weaving"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity}/participants",
        params={"email": "michael@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
