import os
import base64
import requests


class SessionHandler:
    def __init__(self, username: str = None, password: str = None) -> None:
        self.session: requests.Session | None = None
        self.session_headers: dict = {
            "Accept-Language": "en", "Accept": "application/json"}
        self.session_key: str | None = None

        # Let environment variables have priority
        if (os.environ.get("NORDNET_USERNAME") is not None):
            self.username = os.environ["NORDNET_USERNAME"]
        else:
            self.username = username

        if (os.environ.get("NORDNET_PASSWORD") is not None):
            self.password = os.environ["NORDNET_PASSWORD"]
        else:
            self.password = password

    def get_session(self) -> requests.Session:
        if (self.session is None):
            raise NoSessionException("No session is active")
        return self.session

    def login(self) -> None:
        if (self.username is None or self.password is None):
            raise NoCredentialsException("Username or password not found")
        self._prepare_session_for_authentication()
        self._authenticate()

    def _authenticate(self) -> None:
        url = "https://www.nordnet.dk/api/2/authentication/basic/login"
        payload = {"username": self.username, "password": self.password}
        res = self.session.post(url=url,  data=payload).json()
        self.session_key = res["session_key"]

    def _prepare_session_for_authentication(self) -> None:
        if (self.session is None):
            self._create_session()
        self.session.get("https://nordnet.dk/logind")

        self.session.headers["client-id"] = "NEXT"
        self.session.headers["sub-client-id"] = "NEXT"

    def _create_session(self) -> None:
        self.session = requests.Session()
        self.session.headers = self.session_headers


class NoCredentialsException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(message)


class NoSessionException(Exception):
    def __init__(self, message):
        super().__init__(message)
        print(message)
