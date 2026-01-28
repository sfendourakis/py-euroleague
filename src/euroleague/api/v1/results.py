"""V1 Results API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class ResultsAPI(BaseAPI):
    """
    V1 Results API for retrieving game results.

    Example:
        >>> results_api.get(season_code="E2024", game_number=10)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Results API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "v1/results")

    def get(
        self,
        season_code: str,
        game_number: int | None = None,
    ) -> dict[str, Any]:
        """Get all games played in a season after a specific game number.

        Args:
            season_code: Season code (e.g., 'E2024')
            game_number: Optional game number to filter results from

        Returns:
            Game results data
        """
        params: dict[str, Any] = {"seasonCode": season_code}
        if game_number is not None:
            params["gameNumber"] = game_number
        return self._get(params=params)

    async def get_async(
        self,
        season_code: str,
        game_number: int | None = None,
    ) -> dict[str, Any]:
        """Get all games played in a season after a specific game number (async).

        Args:
            season_code: Season code (e.g., 'E2024')
            game_number: Optional game number to filter results from

        Returns:
            Game results data
        """
        params: dict[str, Any] = {"seasonCode": season_code}
        if game_number is not None:
            params["gameNumber"] = game_number
        return await self._get_async(params=params)
