"""Common/shared models used across API versions."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import Field, HttpUrl

from euroleague.models.base import EuroleagueModel


class Competition(EuroleagueModel):
    """Competition information."""

    code: str = Field(..., alias="competitionCode", description="Competition code (e.g., 'E')")
    name: str = Field(..., alias="competitionName")
    alias: Optional[str] = Field(None, alias="competitionAlias")


class Season(EuroleagueModel):
    """Season information."""

    code: str = Field(..., alias="seasonCode", description="Season code (e.g., 'E2024')")
    year: Optional[int] = None
    name: Optional[str] = None
    is_current: bool = Field(False, alias="isCurrent")
    start_date: Optional[date] = Field(None, alias="startDate")
    end_date: Optional[date] = Field(None, alias="endDate")


class Club(EuroleagueModel):
    """Club/team information."""

    code: str = Field(..., alias="clubCode")
    name: str = Field(..., alias="clubName")
    alias: Optional[str] = Field(None, alias="clubAlias")
    city: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = Field(None, alias="countryCode")
    arena: Optional[str] = Field(None, alias="arenaName")
    arena_capacity: Optional[int] = Field(None, alias="arenaCapacity")
    website: Optional[str] = None
    logo_url: Optional[str] = Field(None, alias="logoUrl")
    primary_color: Optional[str] = Field(None, alias="primaryColor")
    secondary_color: Optional[str] = Field(None, alias="secondaryColor")


class Person(EuroleagueModel):
    """Base person information (player, coach, referee)."""

    code: str = Field(..., alias="personCode")
    name: str = Field(..., alias="personName")
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    birth_date: Optional[date] = Field(None, alias="birthDate")
    country: Optional[str] = None
    country_code: Optional[str] = Field(None, alias="countryCode")
    height: Optional[int] = Field(None, description="Height in cm")
    weight: Optional[int] = Field(None, description="Weight in kg")
    image_url: Optional[str] = Field(None, alias="imageUrl")


class Player(Person):
    """Player information."""

    position: Optional[str] = None
    jersey_number: Optional[str] = Field(None, alias="jerseyNumber")
    is_active: bool = Field(True, alias="isActive")


class Coach(Person):
    """Coach information."""

    role: Optional[str] = None


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
    phase_type: Optional[str] = Field(None, alias="phaseTypeCode")
    group: Optional[str] = Field(None, alias="groupName")
    date: Optional[datetime] = Field(None, alias="gameDate")
    status: Optional[str] = None
    home_team: Optional[Club] = Field(None, alias="homeTeam")
    away_team: Optional[Club] = Field(None, alias="awayTeam")
    home_team_code: Optional[str] = Field(None, alias="homeTeamCode")
    away_team_code: Optional[str] = Field(None, alias="awayTeamCode")
    home_score: Optional[int] = Field(None, alias="homeScore")
    away_score: Optional[int] = Field(None, alias="awayScore")
    arena: Optional[str] = None
    attendance: Optional[int] = None


class Phase(EuroleagueModel):
    """Phase/stage of a season."""

    code: str = Field(..., alias="phaseTypeCode")
    name: str = Field(..., alias="phaseTypeName")
    alias: Optional[str] = Field(None, alias="phaseTypeAlias")


class Round(EuroleagueModel):
    """Round information within a phase."""

    number: int = Field(..., alias="roundNumber")
    name: Optional[str] = Field(None, alias="roundName")
    start_date: Optional[date] = Field(None, alias="startDate")
    end_date: Optional[date] = Field(None, alias="endDate")


class Group(EuroleagueModel):
    """Group within a phase."""

    id: int = Field(..., alias="groupId")
    name: str = Field(..., alias="groupName")
    raw_name: Optional[str] = Field(None, alias="groupRawName")


class Standing(EuroleagueModel):
    """Team standing in a round/group."""

    position: int
    club: Optional[Club] = None
    club_code: Optional[str] = Field(None, alias="clubCode")
    club_name: Optional[str] = Field(None, alias="clubName")
    games_played: int = Field(0, alias="gamesPlayed")
    wins: int = 0
    losses: int = 0
    points_for: int = Field(0, alias="pointsFor")
    points_against: int = Field(0, alias="pointsAgainst")
    points_difference: int = Field(0, alias="pointsDifference")
    points: int = 0  # Standings points (typically 2*wins + 1*losses in FIBA)


class PlayerStats(EuroleagueModel):
    """Basic player statistics."""

    player: Optional[Person] = None
    player_code: Optional[str] = Field(None, alias="playerCode")
    player_name: Optional[str] = Field(None, alias="playerName")
    team_code: Optional[str] = Field(None, alias="teamCode")
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

    team_code: Optional[str] = Field(None, alias="teamCode")
    team_name: Optional[str] = Field(None, alias="teamName")
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
