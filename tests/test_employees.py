from settings.api_con.users import UserQuery


class TestEmployeeApi:

    UserQuery.format_user_with_hashed_password

    def get_headers(self):
        return {"Content-Type": "application/json"}

    def test_get_all_employee(self, client, get_token):
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {get_token}"
        response = client.get("/api/v1/employee", headers=headers)
        assert response.status_code == 200

    def test_get_all_employee_without_token(self, client, get_token):

        response = client.get("/api/v1/employee", headers=self.get_headers())
        assert response.status_code == 401

    def test_get_one_employee(self, client, get_token):
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {get_token}"
        response = client.get("/api/v1/employee/1", headers=headers)
        assert response.status_code == 200

    def test_update_employee_ok(self, client, get_token, employee_payload):
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {get_token}"
        response = client.patch(
            "/api/v1/employee/1", headers=headers, json=employee_payload
        )
        assert response.status_code == 200

    def test_update_employee_with_wrong_id(
        self, client, get_token, employee_payload
    ):
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {get_token}"
        response = client.patch(
            "/api/v1/employee/5000", headers=headers, json=employee_payload
        )
        assert response.status_code == 404

    def test_update_employee_without_jwt_token(
        self, client, employee_payload
    ):

        response = client.patch(
            "/api/v1/employee/1",
            headers=self.get_headers(),
            json=employee_payload,
        )
        assert response.status_code == 401

    def test_create_employee_csv(self, client, get_token):
        headers = self.get_headers()
        headers["Authorization"] = f"Bearer {get_token}"
        response = client.get("/api/v1/employee/csv", headers=headers)
        assert response.status_code == 200
