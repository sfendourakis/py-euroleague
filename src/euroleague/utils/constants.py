"""Constants and enumerations for the Euroleague API."""

from enum import Enum

# API Base URL
BASE_URL = "https://api-live.euroleague.net"

# OAuth2 endpoints
AUTH_URL = "https://auth.euroleague.net/oauth2/authorize"
TOKEN_URL = "https://auth.euroleague.net/oauth2/token"
OAUTH_SCOPE = "euroleagueapi"


class CompetitionCode(str, Enum):
    """Euroleague competition codes."""

    EUROLEAGUE = "E"
    EUROCUP = "U"


class SeasonMode(str, Enum):
    """Season mode for statistics queries."""

    SINGLE = "Single"
    RANGE = "Range"


class StatisticMode(str, Enum):
    """Statistic aggregation mode."""

    PER_GAME = "PerGame"
    ACCUMULATED = "Accumulated"
    PER_40 = "Per40"


class SortDirection(str, Enum):
    """Sort direction for queries."""

    ASCENDING = "Ascending"
    DESCENDING = "Descending"


class PersonType(str, Enum):
    """Type of person in the database."""

    PLAYER = "Player"
    COACH = "Coach"
    REFEREE = "Referee"


class PhaseType(str, Enum):
    """Phase types in a season."""

    REGULAR_SEASON = "RS"
    PLAYOFFS = "PO"
    FINAL_FOUR = "FF"
    TOP_16 = "TS"
