# -*- coding: utf-8 -*-

"""
This module provides utility functions for the Spotipy application.

It includes functions for parsing scopes, loading JSON data from a file, and saving
JSON data to a file.

Functions
---------
parse_scopes(scopes)
    Parses the scopes from the given input.

load_json(path)
    Loads JSON data from a file.

save_json(path, data, indent)
    Saves JSON data to a file.

create_user_agent(browsers)
    Creates a user agent string based on the provided browsers.

generate_code_verifier(length)
    Generates a code verifier for OAuth 2.0 PKCE.

generate_code_challenge(verifier)
    Generates a code challenge derived from the code verifier.
"""

__all__ = [
    "CLIENT_CREDS_ENV_VARS",
    "create_user_agent",
    "generate_code_challenge",
    "generate_code_verifier",
    "load_json",
    "parse_scopes",
    "save_json",
]

import random
from base64 import urlsafe_b64encode
from functools import singledispatch
from hashlib import sha256
from json import JSONDecodeError
import logging
from pathlib import Path
import typing as t
from string import ascii_letters, digits

from fake_useragent import UserAgent
from orjson import (
    loads as orjson_loads,
    dumps as orjson_dumps,
    OPT_INDENT_2,
)

from custom_types.scope import Scope

LOGGER = logging.getLogger(__name__)

CLIENT_CREDS_ENV_VARS = {
    "client_id": "SPOTIPY_CLIENT_ID",
    "client_secret": "SPOTIPY_CLIENT_SECRET",
    "client_username": "SPOTIPY_CLIENT_USERNAME",
    "redirect_uri": "SPOTIPY_REDIRECT_URI",
}


@singledispatch
def parse_scopes(scopes) -> t.List[Scope]:
    """
    Parses the scopes from the given input.

    This function is a generic function and its behavior depends on the
    type of the `scopes` argument.
    It raises a NotImplementedError for unsupported types.

    Parameters
    ----------
    scopes : variable type
        The input to parse the scopes from.

    Returns
    -------
    list[Scope]
        The parsed scopes.

    Raises
    ------
    NotImplementedError
        If the type of `scopes` is not supported.
    """
    raise NotImplementedError(f"Unsupported type: {type(scopes).__name__}")


@parse_scopes.register
def _(scopes: str) -> t.List[Scope]:
    """
    Parses the scopes from a string.

    The string should contain scope names separated by commas.

    Parameters
    ----------
    scopes : str
        The string to parse the scopes from.

    Returns
    -------
    list[Scope]
        The parsed scopes.
    """
    return [Scope(scope) for scope in scopes.replace(" ", "").split(",")]


@parse_scopes.register
def _(scopes: list) -> t.List[Scope]:
    """
    Parses the scopes from a list of strings.

    Each string in the list should be a scope name.

    Parameters
    ----------
    scopes : list[str]
        The list of strings to parse the scopes from.

    Returns
    -------
    list[Scope]
        The parsed scopes.
    """
    return [Scope(scope) for scope in scopes]


def load_json(*, path: Path) -> t.Dict[str, t.Any]:
    """
    Loads JSON data from a file.

    Parameters
    ----------
    path : Path
        The path to the file to load the JSON data from.

    Returns
    -------
    dict[str, Any]
        The loaded JSON data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    orjson.JSONDecodeError
        If the file does not contain valid JSON.
    """
    if not path.exists():
        raise FileNotFoundError(f"No such file: '{path}'")

    try:
        return orjson_loads(path.read_bytes())
    except JSONDecodeError as e:
        raise ValueError(f"File {path} does not contain valid JSON") from e


def save_json(*, path: Path, data: t.Dict[str, t.Any], indent: bool = True) -> int:
    """
    Saves JSON data to a file.

    Parameters
    ----------
    path : Path
        The path to the file to save the JSON data to.
    data : dict[str, Any]
        The JSON data to save.
    indent : bool, optional
        Whether to indent the JSON data in the file, by default True.

    Returns
    -------
    int
        The number of bytes written to the file.
    """
    if indent:
        indent_option = OPT_INDENT_2
    else:
        indent_option = None
    return path.write_bytes(orjson_dumps(data, option=indent_option))


@singledispatch
def create_user_agent(browsers) -> str:
    """
    Creates a user agent string based on the provided browser.

    This function is a generic function and its behavior depends on the
    type of the `browser` argument.
    It raises a NotImplementedError for unsupported types.

    Parameters
    ----------
    browsers : variable type
        The input to determine the browser for the user agent.

    Returns
    -------
    str
        The generated user agent string.

    Raises
    ------
    NotImplementedError
        If the type of `browser` is not supported.
    """
    raise NotImplementedError(
        f"Unsupported type for browser: {type(browsers).__name__}"
    )


@create_user_agent.register
def _(browsers: list) -> str:
    """
    Creates a user agent string based on the provided list of browsers.

    Parameters
    ----------
    browsers : list
        The list of browsers to use for generating the user agent string.

    Returns
    -------
    str
        The generated user agent string.
    """
    return UserAgent(os="macos", browsers=browsers, platforms="pc").random


@create_user_agent.register
def _(browsers: str) -> str:
    """
    Creates a user agent string based on the provided browser.

    Parameters
    ----------
    browsers : str
        The browser to use for generating the user agent string.

    Returns
    -------
    str
        The generated user agent string.
    """
    agent = UserAgent(os="macos", browsers=[browsers], platforms="pc")
    return agent[browsers]

def generate_code_verifier(length=128) -> str:
    """
    Generates a code verifier for OAuth 2.0 PKCE.

    The code verifier is a cryptographically random string using the
    characters A-Z, a-z, 0-9, and the punctuation characters -._~ (hyphen,
    period, underscore, and tilde), between 43 and 128 characters long.

    Parameters
    ----------
    length : int, optional
        The length of the code verifier, by default 128

    Returns
    -------
    str
        The generated code verifier.
    """
    return "".join(random.choices(ascii_letters + digits, k=length))


def generate_code_challenge(verifier) -> str:
    """
    Generates a code challenge derived from the code verifier.

    This is done by hashing the code verifier with SHA-256, then encoding
    the hash value in URL-safe base64, and removing any padding.

    Parameters
    ----------
    verifier : str
        The code verifier.

    Returns
    -------
    str
        The generated code challenge.
    """
    digest = sha256(verifier.encode("utf-8")).digest()
    return urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")