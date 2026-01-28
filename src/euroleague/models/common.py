"""Common/shared models used across API versions."""

from datetime import date, datetime

from pydantic import Field

from euroleague.models.base import EuroleagueModel


class Competition(EuroleagueModel):
    """Competition information."""

    code: str = Field(..., alias="competitionCode", description="Competition code (e.g., 'E')")
    name: str = Field(..., alias="competitionName")
    alias: str | None = Field(None, alias="competitionAlias")


class Season(EuroleagueModel):
    """Season information."""

    code: str = Field(..., alias="seasonCode", description="Season code (e.g., 'E2024')")
    year: int | None = None
    name: str | None = None
    is_current: bool = Field(False, alias="isCurrent")
    start_date: date | None = Field(None, alias="startDate")
    end_date: date | None = Field(None, alias="endDate")


class Club(EuroleagueModel):
    """Club/team information."""

    code: str = Field(..., alias="clubCode")
    name: str = Field(..., alias="clubName")
    alias: str | None = Field(None, alias="clubAlias")
    city: str | None = None
    country: str | None = None
    country_code: str | None = Field(None, alias="countryCode")
    arena: str | None = Field(None, alias="arenaName")
    arena_capacity: int | None = Field(None, alias="arenaCapacity")
    website: str | None = None
    logo_url: str | None = Field(None, alias="logoUrl")
    primary_color: str | None = Field(None, alias="primaryColor")
    secondary_color: str | None = Field(None, alias="secondaryColor")


class Person(EuroleagueModel):
    """Base person information (player, coach, referee)."""

    code: str = Field(..., alias="personCode")
    name: str = Field(..., alias="personName")
    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    birth_date: date | None = Field(None, alias="birthDate")
    country: str | None = None
    country_code: str | None = Field(None, alias="countryCode")
    height: int | None = Field(None, description="Height in cm")
    weight: int | None = Field(None, description="Weight in kg")
    image_url: str | None = Field(None, alias="imageUrl")


class Player(Person):
    """Player information."""

    position: str | None = None
    jersey_number: str | None = Field(None, alias="jerseyNumber")
    is_active: bool = Field(True, alias="isActive")


class Coach(Person):
    """Coach information."""

    role: str | None = None


class Referee(Person):
    """Referee information."""

    pass


class GameScore(EuroleagueModel):
    """Game score information."""

    home: int = Field(..., alias="homeScore")
    away: int = Field(..., alias="awayScore")

    @property
    def winner(self) -> str:
        """Return 'home' or 'away' based on winner."""
        return "home" if self.home > self.away else "away"

    @property
    def margin(self) -> int:
        """Return absolute score margin."""
        return abs(self.home - self.away)


class Game(EuroleagueModel):
    """Game information."""

    code: int = Field(..., alias="gameCode")
    competition_code: str = Field(..., alias="competitionCode")
    season_code: str = Field(..., alias="seasonCode")
    round_number: int = Field(..., alias="round")
    phase_type: str | None = Field(None, alias="phaseTypeCode")
    group: str | None = Field(None, alias="groupName")
    date: datetime | None = Field(None, alias="gameDate")
    status: str | None = None
    home_team: Club | None = Field(None, alias="homeTeam")
    away_team: Club | None = Field(None, alias="awayTeam")
    home_team_code: str | None = Field(None, alias="homeTeamCode")
    away_team_code: str | None = Field(None, alias="awayTeamCode")
    home_score: int | None = Field(None, alias="homeScore")
    away_score: int | None = Field(None, alias="awayScore")
    arena: str | None = None
    attendance: int | None = None


class Phase(EuroleagueModel):
    """Phase/stage of a season."""

    code: str = Field(..., alias="phaseTypeCode")
    name: str = Field(..., alias="phaseTypeName")
    alias: str | None = Field(None, alias="phaseTypeAlias")


class Round(EuroleagueModel):
    """Round information within a phase."""

    number: int = Field(..., alias="roundNumber")
    name: str | None = Field(None, alias="roundName")
    start_date: date | None = Field(None, alias="startDate")
    end_date: date | None = Field(None, alias="endDate")


class Group(EuroleagueModel):
    """Group within a phase."""

    id: int = Field(..., alias="groupId")
    name: str = Field(..., alias="groupName")
    raw_name: str | None = Field(None, alias="groupRawName")


class Standing(EuroleagueModel):
    """Team standing in a round/group."""

    position: int
    club: Club | None = None
    club_code: str | None = Field(None, alias="clubCode")
    club_name: str | None = Field(None, alias="clubName")
    games_played: int = Field(0, alias="gamesPlayed")
    wins: int = 0
    losses: int = 0
    points_for: int = Field(0, alias="pointsFor")
    points_against: int = Field(0, alias="pointsAgainst")
    points_difference: int = Field(0, alias="pointsDifference")
    points: int = 0  # Standings points (typically 2*wins + 1*losses in FIBA)


class PlayerStats(EuroleagueModel):
    """Basic player statistics."""

    player: Person | None = None
    player_code: str | None = Field(None, alias="playerCode")
    player_name: str | None = Field(None, alias="playerName")
    team_code: str | None = Field(None, alias="teamCode")
    games_played: int = Field(0, alias="gamesPlayed")
    minutes: float = 0.0
    points: float = 0.0
    rebounds: float = 0.0
    offensive_rebounds: float = Field(0.0, alias="offensiveRebounds")
    defensive_rebounds: float = Field(0.0, alias="defensiveRebounds")
    assists: float = 0.0
    steals: float = 0.0
    blocks: float = 0.0
    turnovers: float = 0.0
    fouls: float = Field(0.0, alias="personalFouls")
    field_goals_made: int = Field(0, alias="fieldGoalsMade")
    field_goals_attempted: int = Field(0, alias="fieldGoalsAttempted")
    two_pointers_made: int = Field(0, alias="twoPointersMade")
    two_pointers_attempted: int = Field(0, alias="twoPointersAttempted")
    three_pointers_made: int = Field(0, alias="threePointersMade")
    three_pointers_attempted: int = Field(0, alias="threePointersAttempted")
    free_throws_made: int = Field(0, alias="freeThrowsMade")
    free_throws_attempted: int = Field(0, alias="freeThrowsAttempted")
    pir: float = Field(0.0, alias="pir", description="Performance Index Rating")

    @property
    def field_goal_pct(self) -> float:
        """Field goal percentage."""
        if self.field_goals_attempted == 0:
            return 0.0
        return (self.field_goals_made / self.field_goals_attempted) * 100

    @property
    def three_point_pct(self) -> float:
        """Three-point percentage."""
        if self.three_pointers_attempted == 0:
            return 0.0
        return (self.three_pointers_made / self.three_pointers_attempted) * 100

    @property
    def free_throw_pct(self) -> float:
        """Free throw percentage."""
        if self.free_throws_attempted == 0:
            return 0.0
        return (self.free_throws_made / self.free_throws_attempted) * 100


class TeamStats(EuroleagueModel):
    """Basic team statistics."""

    team_code: str | None = Field(None, alias="teamCode")
    team_name: str | None = Field(None, alias="teamName")
    games_played: int = Field(0, alias="gamesPlayed")
    wins: int = 0
    losses: int = 0
    points_for: float = Field(0.0, alias="pointsFor")
    points_against: float = Field(0.0, alias="pointsAgainst")
    rebounds: float = 0.0
    assists: float = 0.0
    steals: float = 0.0
    blocks: float = 0.0
    turnovers: float = 0.0
