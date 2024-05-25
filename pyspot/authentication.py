from __future__ import annotations
import os
import base64
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import random
import string
import typing as t
import webbrowser
from socketserver import BaseServer

from authlib.integrations.httpx_client import OAuth2Client
from dotenv import load_dotenv
from pendulum import DateTime, from_timestamp
from pydantic_extra_types.pendulum_dt import DateTime as PydanticDateTime
from pydantic import BaseModel, field_validator

from custom_types import Scope, RequestType


load_dotenv()

AUTH_STRING: str = os.getenv("AUTH_STRING", "")
AUTH_URL: str = os.getenv("AUTH_URL", "")
CLIENT_ID: str = os.getenv("CLIENT_ID", "")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "")
REDIRECT_URI: str = os.getenv("REDIRECT_URI", "")
TOKEN_URL: str = os.getenv("TOKEN_URL", "")
default_scopes = [
    "user-follow-read",
    "user-read-private",
    "user-modify-playback-state",
    "user-library-read",
    "user-read-playback-state",
    "user-read-currently-playing",
    "user-read-recently-played",
    "user-read-playback-position",
    "user-top-read",
    "playlist-read-private",
    "playlist-read-collaborative",
]

SCOPES: t.List[Scope] = [Scope(scope) for scope in os.getenv("SCOPES", "").split(",")]


class Token(BaseModel):
    """
    Represents an OAuth2 token for Spotify.
    """

    access_token: str
    token_type: t.Literal["Bearer"]
    expires_in: int
    refresh_token: str
    scope: t.List[Scope]
    expires_at: PydanticDateTime

    @field_validator("expires_at", mode="before")
    def set_expires_at_from_timestamp(cls, v: int) -> DateTime:
        """
        Sets the expiration date and time from a Unix timestamp.
        Parameters
        ----------
        v: int

        Returns
        -------
        DateTime

        """
        if isinstance(v, int):
            return from_timestamp(v)

    @property
    def expired(self) -> bool:
        """
        Checks if the token has expired.

        Returns
        -------
        bool
            True if the token has expired, False otherwise.
        """
        return self.expires_at < DateTime.now()

    def __repr__(self) -> str:
        """
        Returns the string representation of the token.

        Returns
        -------
        str
            The string representation of the token.

        """
        return (
            f"Token(access_token={self.access_token}, "
            f"token_type={self.token_type}, "
            f"expires_at={self.expires_at})"
        )

    def __str__(self) -> str:
        """
        Returns the string representation of the token.

        Returns
        -------
        str
            The string representation of the token.

        """
        return f"{self.token_type} {self.access_token}"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    token: Token

    def __init__(
        self,
        client: SpotifyOAuthClient,
        code_verifier: str,
        request: RequestType,
        client_address: t.Any,
        server: BaseServer
    ):

        super().__init__(request, client_address, server)
    def do_GET(self):
        # Parse the authorization code from the URL
        query = self.path.split("?")[-1]
        params = dict(qc.split("=") for qc in query.split("&"))
        code = params.get("code")

        if code:
            # Exchange the authorization code for an access token
            token_json = client.fetch_token(
                TOKEN_URL, code=code, code_verifier=code_verifier
            )
            self.token = Token(**token_json)
            print("Access token obtained:")

        # Respond to the client
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(
            b"<html><body><h1>Authorization complete. You can close this window.</h1></body></html>"
        )

    def get_token(self) -> Token:
        return self.token


class SpotifyOAuthClient(OAuth2Client):
    """
    An OAuth2 client for Spotify.

    Attributes
    ----------
    client_id : str
        The client ID for the Spotify application.
    client_secret : str
        The client secret for the Spotify application.
    redirect_uri : str
        The redirect URI for the Spotify application.
    scope : list[Scope]
        The scopes to request from the user when authorizing the application.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: t.List[Scope],
    ):
        """
        Initializes a new SpotifyOAuthClient.

        Parameters
        ----------
        client_id : str
            The client ID for the Spotify application.
        client_secret : str
            The client secret for the Spotify application.
        redirect_uri : str
            The redirect URI for the Spotify application.
        scope : list[Scope]
            The scopes to request from the user when authorizing the application.
        """
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
        )

        code_verifier = self.generate_code_verifier()
        code_challenge = self.generate_code_challenge(code_verifier)

        authorization_url = self.create_authorization_url(
            AUTH_URL, code_challenge=code_challenge, code_challenge_method="S256"
        )
        print(f"Please go to {authorization_url} and authorize access.")

        webbrowser.open(authorization_url[0])
        server = HTTPServer(("localhost", 8888), OAuthCallbackHandler)

        server.handle_request()

    @staticmethod
    def generate_code_verifier(length=128) -> str:
        """
        Generates a code verifier.

        Parameters
        ----------
        length : int, optional
            The length of the code verifier, by default 128

        Returns
        -------
        str
            The generated code verifier.
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_code_challenge(verifier) -> str:
        """
        Generates a code challenge.

        Parameters
        ----------
        verifier : str
            The code verifier.

        Returns
        -------
        str
            The generated code challenge.
        """
        digest = hashlib.sha256(verifier.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")




if __name__ == "__main__":
    ...
