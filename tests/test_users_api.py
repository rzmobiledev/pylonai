from flask import jsonify, make_response
from settings.api_con.users import User


class TestUsersApi:

    headers = {"Content-Type": "application/json"}

    def get_user_by_email(self, email: str):
        user = User.query.filter_by(email=email).first()
        return make_response(jsonify({"user": user.json()}), 200)

    def test_get_homepage(self, client):
        response = client.get("/api/v1/user")
        assert response.status_code == 404

    def test_get_user(self, client):
        response = client.get("/api/v1/user/users")
        assert response.status_code == 200

    def test_create_user(self, client, random_user: dict):
        response = client.post("/api/v1/user/users", headers=self.headers, json=random_user)
        assert response.status_code == 201

    def test_get_single_user(self, client, pylon_user: dict):

        response = client.post("/api/v1/user/users", headers=self.headers, json=pylon_user)
        print(response.json)
        assert response.status_code == 201

        user = self.get_user_by_email(pylon_user.get("email"))
        user.json["user"].get("email") == pylon_user.get("email")
