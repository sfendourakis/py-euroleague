"""V2 Games API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class GamesAPI(BaseAPI):
    """
    V2 Games API for retrieving game information.

    Example:
        >>> games_api.list("E", "2024")
        >>> games_api.get("E", "2024", 1)
        >>> games_api.get_history("E", "2024", 1)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Games API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: Optional[str] = None,
        round_number: Optional[int] = None,
        group_name: Optional[str] = None,
        group_id: Optional[int] = None,
        team_code: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get games for a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            phase_type_code: Optional phase type filter
            round_number: Optional round number filter
            group_name: Optional group name filter
            group_id: Optional group ID filter
            team_code: Optional team code filter
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of games
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "games",
            params={
                "phaseTypeCode": phase_type_code,
                "roundNumber": round_number,
                "groupName": group_name,
                "groupId": group_id,
                "teamCode": team_code,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def list_async(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: Optional[str] = None,
        round_number: Optional[int] = None,
        group_name: Optional[str] = None,
        group_id: Optional[int] = None,
        team_code: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get games for a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "games",
            params={
                "phaseTypeCode": phase_type_code,
                "roundNumber": round_number,
                "groupName": group_name,
                "groupId": group_id,
                "teamCode": team_code,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    def get(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get specific game details.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            game_code: Game code/number

        Returns:
            Game details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
        )

    async def get_async(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get specific game details (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
        )

    def get_history(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get game history (head-to-head).

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            game_code: Game code/number

        Returns:
            Historical game data between the two teams
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "history",
        )

    async def get_history_async(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get game history (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "history",
        )
