from fastapi.testclient import TestClient

from main import app


def test_index():
    client = TestClient(app)
    response = client.get('/chat')
    assert response.status_code == 200    


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect('/chat') as websocket:        
        websocket.send_json({'message': 'Hello:)'})
        data = websocket.receive_json()
        assert data == {
            'msg_number': 1,
            'message': 'Hello:)'
            }        