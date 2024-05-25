from enum import Enum
import typing as t

from pydantic import BaseModel

__all__ = ["Scope"]


class Scope(Enum):
    """
    An enumeration class that defines various scopes for a Spotify
    application.

    Each member of this enum represents a specific scope that can be
    requested from the user when they are authorizing the application.
    The value of each member is the string that needs to be included in
    the authorization request.

    Attributes
    ----------
    APP_REMOTE_CONTROL : str
        Control playback of a Spotify track on the user's device.
    PLAYLIST_MODIFY_PRIVATE : str
        Write access to a user's private playlists.
    PLAYLIST_MODIFY_PUBLIC : str
        Write access to a user's public playlists.
    PLAYLIST_READ_COLLABORATIVE : str
        Include collaborative playlists when requesting a user's
        playlists.
    PLAYLIST_READ_PRIVATE : str
        Read access to a user's private playlists.
    STREAMING : str
        Control playback of a Spotify track on the user's device.
    UGC_IMAGE_UPLOAD : str
        Upload images to Spotify on behalf of the user.
    USER_FOLLOW_MODIFY : str
        Write/delete access to the list of artists and other users that
        the user follows.
    USER_FOLLOW_READ : str
        Read access to the list of artists and other users that the user
        follows.
    USER_LIBRARY_MODIFY : str
        Write/delete access to a user's "Your Music" library.
    USER_LIBRARY_READ : str
        Read access to a user's "Your Music" library.
    USER_MODIFY_PLAYBACK_STATE : str
        Write access to a user's playback state.
    USER_READ_CURRENTLY_PLAYING : str
        Read access to a user's currently playing track.
    USER_READ_EMAIL : str
        Read access to a user's email address.
    USER_READ_PLAYBACK_POSITION : str
        Read access to a user's playback position in a playing context.
    USER_READ_PLAYBACK_STATE : str
        Read access to a user's player state.
    USER_READ_PRIVATE : str
        Read access to a user's subscription details (type of user
        account).
    USER_READ_RECENTLY_PLAYED : str
        Read access to a user's recently played tracks.
    USER_TOP_READ : str
        Read access to a user's top artists and tracks.
    """

    APP_REMOTE_CONTROL = "app-remote-control"
    PLAYLIST_MODIFY_PRIVATE = "playlist-modify-private"
    PLAYLIST_MODIFY_PUBLIC = "playlist-modify-public"
    PLAYLIST_READ_COLLABORATIVE = "playlist-read-collaborative"
    PLAYLIST_READ_PRIVATE = "playlist-read-private"
    STREAMING = "streaming"
    UGC_IMAGE_UPLOAD = "ugc-image-upload"
    USER_FOLLOW_MODIFY = "user-follow-modify"
    USER_FOLLOW_READ = "user-follow-read"
    USER_LIBRARY_MODIFY = "user-library-modify"
    USER_LIBRARY_READ = "user-library-read"
    USER_MODIFY_PLAYBACK_STATE = "user-modify-playback-state"
    USER_READ_CURRENTLY_PLAYING = "user-read-currently-playing"
    USER_READ_EMAIL = "user-read-email"
    USER_READ_PLAYBACK_POSITION = "user-read-playback-position"
    USER_READ_PLAYBACK_STATE = "user-read-playback-state"
    USER_READ_PRIVATE = "user-read-private"
    USER_READ_RECENTLY_PLAYED = "user-read-recently-played"
    USER_TOP_READ = "user-top-read"

    def __str__(self) -> str:
        """
        Returns the string representation of the scope.
        Returns
        -------
        str
            The string representation of the scope.

        """
        return self.value


class ScopeCollection(BaseModel):
    """
    A collection of scopes that can be requested from the user when
    authorizing a Spotify application.

    This class is a Pydantic model that represents a collection of scopes
    that can berequested from the user when authorizing a Spotify
    application. The class provides a method for converting the
    collection of scopes into a single string that can be included in
    the authorization request.

    Attributes
    ----------
    scopes : list[Scope]
        A list of scopes that can be requested from the user when
        authorizing the application.
    """

    scopes: list[Scope]

    def __str__(self) -> str:
        return " ".join(map(str, self.scopes))

    def string_list(self) -> t.List[str]:
        """
        Returns a list of strings representing the scopes in the
        collection.

        Returns
        -------
        list[str]
            A list of strings representing the scopes in the collection.

        """
        return [str(scope) for scope in self.scopes]
