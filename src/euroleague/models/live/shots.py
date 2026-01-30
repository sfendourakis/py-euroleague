"""Pydantic models for shot/points API responses."""

from pydantic import Field, field_validator

from euroleague.models.base import EuroleagueModel


class Shot(EuroleagueModel):
    """A single shot attempt with location data.

    Attributes:
        num_anot: Sequential annotation number
        team: Team identifier (may be padded with spaces)
        player_id: Player identifier code
        player: Player name (LASTNAME, FIRSTNAME format)
        action_id: Action type code (2FGM, 2FGA, 3FGM, 3FGA, FTM, FTA)
        action: Human-readable action description
        points: Points awarded (0, 1, 2, or 3)
        coord_x: X-axis coordinate (-1 for free throws)
        coord_y: Y-axis coordinate (-1 for free throws)
        zone: Court zone letter (A-I, blank for free throws)
        fastbreak: Whether this was a fastbreak play
        second_chance: Whether this was a second-chance point
        points_off_turnover: Whether this was points off turnover
        minute: Game minute when shot occurred
        console: Clock display (MM:SS format)
        points_a: Team A running score after this shot
        points_b: Team B running score after this shot
        utc: Timestamp (YYYYMMDDhhmmss format)
    """

    num_anot: int = Field(alias="NUM_ANOT")
    team: str = Field(alias="TEAM")
    player_id: str = Field(alias="ID_PLAYER")
    player: str = Field(alias="PLAYER")
    action_id: str = Field(alias="ID_ACTION")
    action: str = Field(alias="ACTION")
    points: int = Field(alias="POINTS")
    coord_x: int = Field(alias="COORD_X")
    coord_y: int = Field(alias="COORD_Y")
    zone: str = Field(default="", alias="ZONE")
    fastbreak: bool = Field(default=False, alias="FASTBREAK")
    second_chance: bool = Field(default=False, alias="SECOND_CHANCE")
    points_off_turnover: bool = Field(default=False, alias="POINTS_OFF_TURNOVER")
    minute: int = Field(alias="MINUTE")
    console: str = Field(alias="CONSOLE")
    points_a: int = Field(alias="POINTS_A")
    points_b: int = Field(alias="POINTS_B")
    utc: str = Field(default="", alias="UTC")

    @field_validator("fastbreak", "second_chance", "points_off_turnover", mode="before")
    @classmethod
    def convert_int_to_bool(cls, v: int | bool) -> bool:
        """Convert integer (0/1) to boolean."""
        if isinstance(v, bool):
            return v
        return bool(v)

    @property
    def is_made(self) -> bool:
        """Check if shot was made."""
        return self.action_id in ("2FGM", "3FGM", "FTM")

    @property
    def is_missed(self) -> bool:
        """Check if shot was missed."""
        return self.action_id in ("2FGA", "3FGA", "FTA")

    @property
    def is_three_pointer(self) -> bool:
        """Check if this is a 3-point attempt."""
        return self.action_id in ("3FGM", "3FGA")

    @property
    def is_two_pointer(self) -> bool:
        """Check if this is a 2-point attempt."""
        return self.action_id in ("2FGM", "2FGA")

    @property
    def is_free_throw(self) -> bool:
        """Check if this is a free throw."""
        return self.action_id in ("FTM", "FTA")

    @property
    def has_coordinates(self) -> bool:
        """Check if shot has valid coordinates (not free throw)."""
        return self.coord_x >= 0 and self.coord_y >= 0

    @property
    def team_code(self) -> str:
        """Get team code with whitespace stripped."""
        return self.team.strip()


class ShotsResponse(EuroleagueModel):
    """Response containing all shots for a game.

    Attributes:
        rows: List of all shot attempts in the game
    """

    rows: list[Shot] = Field(default_factory=list, alias="Rows")

    @property
    def all_shots(self) -> list[Shot]:
        """Get all shots."""
        return self.rows

    @property
    def total_shots(self) -> int:
        """Get total number of shots."""
        return len(self.rows)

    @property
    def made_shots(self) -> list[Shot]:
        """Get only made shots."""
        return [s for s in self.rows if s.is_made]

    @property
    def missed_shots(self) -> list[Shot]:
        """Get only missed shots."""
        return [s for s in self.rows if s.is_missed]

    @property
    def field_goals(self) -> list[Shot]:
        """Get field goal attempts (excludes free throws)."""
        return [s for s in self.rows if not s.is_free_throw]

    @property
    def three_pointers(self) -> list[Shot]:
        """Get all 3-point attempts."""
        return [s for s in self.rows if s.is_three_pointer]

    @property
    def two_pointers(self) -> list[Shot]:
        """Get all 2-point attempts."""
        return [s for s in self.rows if s.is_two_pointer]

    @property
    def free_throws(self) -> list[Shot]:
        """Get all free throw attempts."""
        return [s for s in self.rows if s.is_free_throw]

    def get_shots_by_team(self, team_code: str) -> list[Shot]:
        """Get shots for a specific team.

        Args:
            team_code: Team code to filter by

        Returns:
            List of shots for that team
        """
        return [s for s in self.rows if s.team_code == team_code.strip()]

    def get_shots_by_player(self, player_id: str) -> list[Shot]:
        """Get shots for a specific player.

        Args:
            player_id: Player ID to filter by

        Returns:
            List of shots for that player
        """
        return [s for s in self.rows if s.player_id == player_id]

    def get_shots_by_zone(self, zone: str) -> list[Shot]:
        """Get shots from a specific court zone.

        Args:
            zone: Court zone letter (A-I)

        Returns:
            List of shots from that zone
        """
        return [s for s in self.rows if s.zone == zone]

    def get_shooting_percentage(self, shots: list[Shot] | None = None) -> float:
        """Calculate shooting percentage for given shots.

        Args:
            shots: List of shots to calculate percentage for.
                   If None, uses all shots.

        Returns:
            Shooting percentage (0.0 to 100.0)
        """
        if shots is None:
            shots = self.rows
        if not shots:
            return 0.0
        made = sum(1 for s in shots if s.is_made)
        return (made / len(shots)) * 100

    def get_field_goal_percentage(self) -> float:
        """Calculate field goal percentage (excludes free throws)."""
        return self.get_shooting_percentage(self.field_goals)

    def get_three_point_percentage(self) -> float:
        """Calculate 3-point shooting percentage."""
        return self.get_shooting_percentage(self.three_pointers)

    def get_free_throw_percentage(self) -> float:
        """Calculate free throw percentage."""
        return self.get_shooting_percentage(self.free_throws)
