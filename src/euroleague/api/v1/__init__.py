"""V1 API endpoints (legacy/simple)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from euroleague.api.v1.games import GamesAPI
from euroleague.api.v1.players import PlayersAPI
from euroleague.api.v1.results import ResultsAPI
from euroleague.api.v1.schedules import SchedulesAPI
from euroleague.api.v1.standings import StandingsAPI
from euroleague.api.v1.teams import TeamsAPI

if TYPE_CHECKING:
    from euroleague.http import AsyncHTTPClient, HTTPClient


class V1API:
    """
    Namespace for V1 API endpoints (legacy/simple).

    V1 provides basic access to game box scores, player stats,
    results, schedules, standings, and team rosters.

    Example:
        >>> client.v1.games.get(season_code="E2024", game_code=1)
        >>> client.v1.standings.get(season_code="E2024")
    """

    def __init__(self, http_client: HTTPClient | AsyncHTTPClient) -> None:
        """Initialize V1 API namespace.

        Args:
            http_client: HTTP client for making requests
        """
        self.games = GamesAPI(http_client)
        self.players = PlayersAPI(http_client)
        self.results = ResultsAPI(http_client)
        self.schedules = SchedulesAPI(http_client)
        self.standings = StandingsAPI(http_client)
        self.teams = TeamsAPI(http_client)


__all__ = [
    "V1API",
    "GamesAPI",
    "PlayersAPI",
    "ResultsAPI",
    "SchedulesAPI",
    "StandingsAPI",
    "TeamsAPI",
]
