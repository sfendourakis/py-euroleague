"""V3 Games API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class GamesAPI(BaseAPI):
    """
    V3 Games API for retrieving game reports and statistics.

    Example:
        >>> games_api.get_report("E", "2024", 1)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Games API."""
        super().__init__(http_client, "v3/competitions")

    def get_report(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get match report.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            game_code: Game code/number

        Returns:
            Match report
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "report",
        )

    async def get_report_async(
        self,
        competition_code: str,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get match report (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "games",
            str(game_code),
            "report",
        )
