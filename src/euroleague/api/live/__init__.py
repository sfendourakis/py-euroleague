"""Live API namespace for real-time Euroleague data."""

from __future__ import annotations

from typing import TYPE_CHECKING

from euroleague.api.live.play_by_play import PlayByPlayAPI

if TYPE_CHECKING:
    from euroleague.http import AsyncHTTPClient, HTTPClient


class LiveAPI:
    """Live API namespace for real-time game data.

    Provides access to live game data endpoints including play-by-play.

    Attributes:
        play_by_play: Play-by-play data API
    """

    def __init__(self, http_client: HTTPClient | AsyncHTTPClient) -> None:
        """Initialize the Live API namespace.

        Args:
            http_client: HTTP client configured for live API base URL
        """
        self.play_by_play = PlayByPlayAPI(http_client)


__all__ = ["LiveAPI", "PlayByPlayAPI"]
