from flask import jsonify, make_response
from settings.api_con.users import User, UserQuery


class TestUsersApi:

    UserQuery.format_user_with_hashed_password

    def get_headers(self):
        return {"Content-Type": "application/json"}

    def get_user_by_email(self, email: str):
        user = User.query.filter_by(email=email).first()
        return make_response(jsonify({"user": user.json()}), 200)

    def test_get_homepage(self, client):
        response = client.get("/api/v1/user")
        assert response.status_code == 404

    def test_get_user_without_jwt_token(self, client):

        response = client.get("/api/v1/user/users", headers=self.get_headers())
        assert response.status_code == 401

    def test_get_user(self, client, get_token):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {get_token}",
        }
        response = client.get("/api/v1/user/users", headers=headers)
        assert response.status_code == 200

    def test_create_user(self, client, random_user: dict, get_token):
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {get_token}"

        response = client.post(
            "/api/v1/user/users", headers=headers, json=random_user
        )
        assert response.status_code == 201

    def test_get_single_user(self, client, pylon_user: dict, get_token):
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {get_token}"

        response = client.post(
            "/api/v1/user/users", headers=headers, json=pylon_user
        )
        print(response.json)
        assert response.status_code == 201

        user = self.get_user_by_email(pylon_user.get("email"))
        user.json["user"].get("email") == pylon_user.get("email")
