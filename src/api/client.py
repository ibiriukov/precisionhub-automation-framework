import requests


class ApiClient:
    def __init__(self, base_url: str, timeout_s: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.session = requests.Session()

    def get(self, path: str, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        return self.session.get(url, timeout=self.timeout_s, **kwargs)