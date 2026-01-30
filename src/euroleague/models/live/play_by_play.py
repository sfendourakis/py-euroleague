"""Pydantic models for play-by-play API responses."""

from pydantic import Field

from euroleague.models.base import EuroleagueModel


class PlayEvent(EuroleagueModel):
    """A single play event in a game.

    Attributes:
        number_of_play: Sequential play identifier
        play_type: Action type code (e.g., '2FGM', '3FGA', 'AS', 'TO', 'ST')
        player: Player name (may be None for team events)
        player_id: Unique player identifier
        team: Team name (may be None)
        team_code: Team code identifier
        dorsal: Jersey number
        minute: Quarter minute when play occurred
        marker_time: Clock time in MM:SS format
        points_a: Team A score after this play
        points_b: Team B score after this play
        play_info: Human-readable play description
        comment: Additional notes
        event_type: Event classification (0 = standard play)
    """

    number_of_play: int = Field(alias="NUMBEROFPLAY")
    play_type: str = Field(alias="PLAYTYPE")
    player: str | None = Field(default=None, alias="PLAYER")
    player_id: str = Field(alias="PLAYER_ID")
    team: str | None = Field(default=None, alias="TEAM")
    team_code: str = Field(alias="CODETEAM")
    dorsal: str | None = Field(default=None, alias="DORSAL")
    minute: int = Field(alias="MINUTE")
    marker_time: str = Field(alias="MARKERTIME")
    points_a: int | None = Field(default=None, alias="POINTS_A")
    points_b: int | None = Field(default=None, alias="POINTS_B")
    play_info: str = Field(default="", alias="PLAYINFO")
    comment: str = Field(default="", alias="COMMENT")
    event_type: int = Field(default=0, alias="TYPE")

    @property
    def is_scoring_play(self) -> bool:
        """Check if this is a scoring play (made shot or free throw)."""
        return self.play_type in ("2FGM", "3FGM", "FTM")

    @property
    def is_shot_attempt(self) -> bool:
        """Check if this is any shot attempt."""
        return self.play_type in ("2FGM", "2FGA", "3FGM", "3FGA", "FTM", "FTA")

    @property
    def points_scored(self) -> int:
        """Get points scored on this play (0 if not a scoring play)."""
        if self.play_type == "3FGM":
            return 3
        elif self.play_type == "2FGM":
            return 2
        elif self.play_type == "FTM":
            return 1
        return 0


class PlayByPlayResponse(EuroleagueModel):
    """Full play-by-play response for a game.

    Attributes:
        live: Whether the game is currently live
        team_a: Home team name
        team_b: Away team name
        code_team_a: Home team code
        code_team_b: Away team code
        actual_quarter: Current quarter (for live games)
        first_quarter: List of plays in Q1
        second_quarter: List of plays in Q2
        third_quarter: List of plays in Q3
        fourth_quarter: List of plays in Q4
        extra_time: List of plays in overtime (if applicable)
    """

    live: bool = Field(alias="Live")
    team_a: str = Field(alias="TeamA")
    team_b: str = Field(alias="TeamB")
    code_team_a: str = Field(alias="CodeTeamA")
    code_team_b: str = Field(alias="CodeTeamB")
    actual_quarter: int = Field(alias="ActualQuarter")
    first_quarter: list[PlayEvent] = Field(default_factory=list, alias="FirstQuarter")
    second_quarter: list[PlayEvent] = Field(default_factory=list, alias="SecondQuarter")
    third_quarter: list[PlayEvent] = Field(default_factory=list, alias="ThirdQuarter")
    fourth_quarter: list[PlayEvent] = Field(default_factory=list, alias="FourthQuarter")
    extra_time: list[PlayEvent] = Field(default_factory=list, alias="ExtraTime")

    @property
    def all_plays(self) -> list[PlayEvent]:
        """Get all plays across all quarters in chronological order."""
        return (
            self.first_quarter
            + self.second_quarter
            + self.third_quarter
            + self.fourth_quarter
            + self.extra_time
        )

    @property
    def total_plays(self) -> int:
        """Get total number of plays in the game."""
        return len(self.all_plays)

    def get_quarter(self, quarter: int) -> list[PlayEvent]:
        """Get plays for a specific quarter (1-4, 5 for overtime).

        Args:
            quarter: Quarter number (1-4, or 5 for overtime)

        Returns:
            List of plays for that quarter
        """
        quarter_map = {
            1: self.first_quarter,
            2: self.second_quarter,
            3: self.third_quarter,
            4: self.fourth_quarter,
            5: self.extra_time,
        }
        return quarter_map.get(quarter, [])

    def get_plays_by_team(self, team_code: str) -> list[PlayEvent]:
        """Get all plays for a specific team.

        Args:
            team_code: Team code to filter by

        Returns:
            List of plays for that team
        """
        return [p for p in self.all_plays if p.team_code.strip() == team_code.strip()]

    def get_plays_by_player(self, player_id: str) -> list[PlayEvent]:
        """Get all plays for a specific player.

        Args:
            player_id: Player ID to filter by

        Returns:
            List of plays for that player
        """
        return [p for p in self.all_plays if p.player_id == player_id]

    def get_scoring_plays(self) -> list[PlayEvent]:
        """Get all scoring plays in the game."""
        return [p for p in self.all_plays if p.is_scoring_play]
