"""V1 Standings API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class StandingsAPI(BaseAPI):
    """
    V1 Standings API for retrieving league standings.

    Example:
        >>> standings_api.get(season_code="E2024", game_number=10)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Standings API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "v1/standings")

    def get(
        self,
        season_code: str,
        game_number: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get standings in all groups of all stages in a season.

        Args:
            season_code: Season code (e.g., 'E2024')
            game_number: Optional round number for standings snapshot

        Returns:
            Standings data for all groups and stages
        """
        params: dict[str, Any] = {"seasonCode": season_code}
        if game_number is not None:
            params["gameNumber"] = game_number
        return self._get(params=params)

    async def get_async(
        self,
        season_code: str,
        game_number: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get standings in all groups of all stages in a season (async).

        Args:
            season_code: Season code (e.g., 'E2024')
            game_number: Optional round number for standings snapshot

        Returns:
            Standings data for all groups and stages
        """
        params: dict[str, Any] = {"seasonCode": season_code}
        if game_number is not None:
            params["gameNumber"] = game_number
        return await self._get_async(params=params)
