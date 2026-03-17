from src.api.client import ApiClient


class UsersApi:
    def __init__(self, client: ApiClient):
        self.client = client

    def list_users(self):
        return self.client.get("/users")

    def get_user(self, user_id: int):
        return self.client.get(f"/users/{user_id}")