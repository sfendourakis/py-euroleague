"""V3 Stats API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class StatsAPI(BaseAPI):
    """
    V3 Stats API for retrieving game and club statistics.

    Example:
        >>> stats_api.get_player_leaders("E")
        >>> stats_api.get_game_stats("E", "2024", 1)
        >>> stats_api.get_teams_comparison("E", "2024", 1)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Stats API."""
        super().__init__(http_client, "v3/competitions")

    def get_player_leaders(
        self,
        competition_code: str,
        max_round: Optional[int] = None,
        round_number: Optional[int] = None,
        club_code: Optional[str] = None,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        category: Optional[str] = None,
        aggregate: Optional[str] = None,
        misc: Optional[str] = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get player leaders statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            max_round: Maximum round to include
            round_number: Specific round number
            club_code: Club code filter
            season_mode: Season mode (Single/Range)
            season_code: Season code
            category: Statistic category
            aggregate: Aggregation type
            misc: Miscellaneous filter
            limit: Maximum number of results

        Returns:
            Player leaders statistics
        """
        return self._get(
            competition_code,
            "stats",
            "players",
            "leaders",
            params={
                "maxRound": max_round,
                "round": round_number,
                "clubCode": club_code,
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    async def get_player_leaders_async(
        self,
        competition_code: str,
        max_round: Optional[int] = None,
        round_number: Optional[int] = None,
        club_code: Optional[str] = None,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        category: Optional[str] = None,
        aggregate: Optional[str] = None,
        misc: Optional[str] = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get player leaders statistics (async)."""
        return await self._get_async(
            competition_code,
            "stats",
            "players",
            "leaders",
            params={
                "maxRound": max_round,
                "round": round_number,
                "clubCode": club_code,
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    def get_club_stats(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        max_round: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get club season statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            club_code: Club code (e.g., 'BAR')
            max_round: Maximum round to include

        Returns:
            Club aggregated statistics
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "stats",
            params={"maxRound": max_round},
        )

    async def get_club_stats_async(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        max_round: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get club season statistics (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "stats",
            params={"maxRound": max_round},
        )

    def get_game_stats(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get game statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            game_code: Game code/number

        Returns:
            Game statistics for both teams
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "stats",
        )

    async def get_game_stats_async(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get game statistics (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "stats",
        )

    def get_teams_comparison(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get pre-game team comparison.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            game_code: Game code/number

        Returns:
            Team comparison statistics
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "teamsComparison",
        )

    async def get_teams_comparison_async(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get pre-game team comparison (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "teamsComparison",
        )
