"""V2 API endpoints (comprehensive)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from euroleague.api.v2.clubs import ClubsAPI
from euroleague.api.v2.competitions import CompetitionsAPI
from euroleague.api.v2.games import GamesAPI
from euroleague.api.v2.groups import GroupsAPI
from euroleague.api.v2.people import PeopleAPI
from euroleague.api.v2.phases import PhasesAPI
from euroleague.api.v2.records import RecordsAPI
from euroleague.api.v2.referees import RefereesAPI
from euroleague.api.v2.rounds import RoundsAPI
from euroleague.api.v2.season_clubs import SeasonClubsAPI
from euroleague.api.v2.season_people import SeasonPeopleAPI
from euroleague.api.v2.seasons import SeasonsAPI
from euroleague.api.v2.standings import StandingsAPI
from euroleague.api.v2.stats import StatsAPI

if TYPE_CHECKING:
    from euroleague.http import AsyncHTTPClient, HTTPClient


class V2API:
    """
    Namespace for V2 API endpoints (comprehensive).

    V2 provides detailed access to clubs, competitions, games, groups,
    people (players/coaches), phases, records, referees, rounds,
    season-specific data, standings, and statistics.

    Example:
        >>> clubs = client.v2.clubs.list()
        >>> games = client.v2.games.list(competition="E", season="2024")
        >>> person = client.v2.people.get("PDEL")
    """

    def __init__(self, http_client: HTTPClient | AsyncHTTPClient) -> None:
        """Initialize V2 API namespace.

        Args:
            http_client: HTTP client for making requests
        """
        self.clubs = ClubsAPI(http_client)
        self.competitions = CompetitionsAPI(http_client)
        self.games = GamesAPI(http_client)
        self.groups = GroupsAPI(http_client)
        self.people = PeopleAPI(http_client)
        self.phases = PhasesAPI(http_client)
        self.records = RecordsAPI(http_client)
        self.referees = RefereesAPI(http_client)
        self.rounds = RoundsAPI(http_client)
        self.season_clubs = SeasonClubsAPI(http_client)
        self.season_people = SeasonPeopleAPI(http_client)
        self.seasons = SeasonsAPI(http_client)
        self.standings = StandingsAPI(http_client)
        self.stats = StatsAPI(http_client)


__all__ = [
    "V2API",
    "ClubsAPI",
    "CompetitionsAPI",
    "GamesAPI",
    "GroupsAPI",
    "PeopleAPI",
    "PhasesAPI",
    "RecordsAPI",
    "RefereesAPI",
    "RoundsAPI",
    "SeasonClubsAPI",
    "SeasonPeopleAPI",
    "SeasonsAPI",
    "StandingsAPI",
    "StatsAPI",
]
