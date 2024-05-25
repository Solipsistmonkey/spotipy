import os
from pathlib import Path
import typing as t

from dotenv import load_dotenv

from custom_types import Scope
from pyspot.utils import parse_scopes

load_dotenv()

AUTH_STRING: str = os.getenv("AUTH_STRING", "")
AUTH_BASE_URL: str = os.getenv("AUTH_URL", "")
CLIENT_ID: str = os.getenv("CLIENT_ID", "")
CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "")
PASSWORD: str = os.getenv("PASSWORD", "")
REDIRECT_URI: str = os.getenv("REDIRECT_URI", "")
USERNAME: str = os.getenv("USERNAME", "")
TOKEN_PATH: Path = Path(os.getenv("TOKEN_PATH", ""))
TOKEN_URL: str = os.getenv("TOKEN_URL", "")

# fmt: off
default_scopes = parse_scopes([
    "user-follow-read", "user-read-private", "user-modify-playback-state",
    "user-library-read", "user-read-playback-state", "user-read-currently-playing",
    "user-read-recently-played", "user-read-playback-position", "user-top-read",
    "playlist-read-private", "playlist-read-collaborative",
])
# fmt: on

SCOPES: t.List[Scope] = parse_scopes(os.getenv("SCOPES", ""))

CHROME = t.Literal["chrome"]
EDGE = t.Literal["edge"]
FIREFOX = t.Literal["firefox"]
SAFARI = t.Literal["safari"]
UserAgentBrowser = t.Union[CHROME, EDGE, FIREFOX, SAFARI]