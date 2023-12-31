# src/tests/test_users.py
import json  # Make sure to import the json module

def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    # First POST request to add the user
    client.post(
        '/users',
        data=json.dumps({
            'username': 'john',
            'email': 'john@algonquincollege.com'
        }),
        content_type='application/json',
    )
    # Second POST request to attempt adding the same user
    resp = client.post(
        '/users',
        data=json.dumps({
            'username': 'john',
            'email': 'john@algonquincollege.com'
        }),
        content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry. That email already exists.' in data['message']
