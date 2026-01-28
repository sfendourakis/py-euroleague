"""V3 API endpoints (statistics-focused)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from euroleague.api.v3.clubs import ClubsAPI
from euroleague.api.v3.coaches import CoachesAPI
from euroleague.api.v3.games import GamesAPI
from euroleague.api.v3.player_stats import PlayerStatsAPI
from euroleague.api.v3.standings import StandingsAPI
from euroleague.api.v3.stats import StatsAPI
from euroleague.api.v3.team_stats import TeamStatsAPI

if TYPE_CHECKING:
    from euroleague.http import AsyncHTTPClient, HTTPClient


class V3API:
    """
    Namespace for V3 API endpoints (statistics-focused).

    V3 provides detailed statistics for players and teams,
    including traditional, advanced, and miscellaneous stats.
    Also includes various standings views.

    Example:
        >>> leaders = client.v3.player_stats.leaders(competition="E")
        >>> traditional = client.v3.player_stats.traditional(competition="E")
        >>> standings = client.v3.standings.basic(competition="E", season="2024", round=10)
    """

    def __init__(self, http_client: HTTPClient | AsyncHTTPClient) -> None:
        """Initialize V3 API namespace.

        Args:
            http_client: HTTP client for making requests
        """
        self.clubs = ClubsAPI(http_client)
        self.coaches = CoachesAPI(http_client)
        self.games = GamesAPI(http_client)
        self.player_stats = PlayerStatsAPI(http_client)
        self.team_stats = TeamStatsAPI(http_client)
        self.standings = StandingsAPI(http_client)
        self.stats = StatsAPI(http_client)


__all__ = [
    "V3API",
    "ClubsAPI",
    "CoachesAPI",
    "GamesAPI",
    "PlayerStatsAPI",
    "TeamStatsAPI",
    "StandingsAPI",
    "StatsAPI",
]
