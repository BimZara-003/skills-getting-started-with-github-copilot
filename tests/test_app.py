from urllib.parse import quote


def test_get_activities_returns_activities(client):
    # Arrange: client fixture
    # Act
    resp = client.get('/activities')
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert 'Chess Club' in data
    assert isinstance(data['Chess Club']['participants'], list)


def test_signup_success_adds_participant(client):
    # Arrange
    activity = 'Chess Club'
    email = 'testuser@mergington.edu'
    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")
    # Assert
    assert resp.status_code == 200
    assert 'Signed up' in resp.json().get('message', '')
    # Verify
    get = client.get('/activities')
    assert email in get.json()[activity]['participants']


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = 'Chess Club'
    existing = 'michael@mergington.edu'
    # Act
    resp = client.post(f"/activities/{quote(activity)}/signup?email={quote(existing)}")
    # Assert
    assert resp.status_code == 400


def test_unregister_success_removes_participant(client):
    # Arrange
    activity = 'Chess Club'
    participant = 'michael@mergington.edu'
    # Act
    resp = client.delete(f"/activities/{quote(activity)}/participants/{quote(participant)}")
    # Assert
    assert resp.status_code == 200
    get = client.get('/activities')
    assert participant not in get.json()[activity]['participants']


def test_unregister_nonexistent_returns_404(client):
    # Arrange
    activity = 'Chess Club'
    participant = 'nonexistent@mergington.edu'
    # Act
    resp = client.delete(f"/activities/{quote(activity)}/participants/{quote(participant)}")
    # Assert
    assert resp.status_code == 404
