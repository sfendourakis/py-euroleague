"""V1 Teams API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class TeamsAPI(BaseAPI):
    """
    V1 Teams API for retrieving club/team information.

    Example:
        >>> teams_api.get(season_code="E2024")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Teams API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "v1/teams")

    def get(
        self,
        season_code: str,
    ) -> dict[str, Any]:
        """Get all clubs with games and roster for a season.

        Args:
            season_code: Season code (e.g., 'E2024')

        Returns:
            All clubs with their rosters and game information
        """
        return self._get(params={"seasonCode": season_code})

    async def get_async(
        self,
        season_code: str,
    ) -> dict[str, Any]:
        """Get all clubs with games and roster for a season (async).

        Args:
            season_code: Season code (e.g., 'E2024')

        Returns:
            All clubs with their rosters and game information
        """
        return await self._get_async(params={"seasonCode": season_code})
