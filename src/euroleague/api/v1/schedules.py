"""V1 Schedules API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class SchedulesAPI(BaseAPI):
    """
    V1 Schedules API for retrieving game schedules.

    Example:
        >>> schedules_api.get(season_code="E2024")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Schedules API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "v1/schedules")

    def get(
        self,
        season_code: str,
        game_number: Optional[int] = None,
    ) -> dict[str, Any]:
        """Get game schedule information.

        Args:
            season_code: Season code (e.g., 'E2024')
            game_number: Optional game number to filter from

        Returns:
            Schedule data with upcoming games
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
        """Get game schedule information (async).

        Args:
            season_code: Season code (e.g., 'E2024')
            game_number: Optional game number to filter from

        Returns:
            Schedule data with upcoming games
        """
        params: dict[str, Any] = {"seasonCode": season_code}
        if game_number is not None:
            params["gameNumber"] = game_number
        return await self._get_async(params=params)
