def test_send_invite(client):
    response = client.post("/send-invite", json={"sender": "john", "recipient": "jane"})
    assert response.status_code == 200
    assert response.json()["message"] == "Invite sent!"
