"""V1 Players API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class PlayersAPI(BaseAPI):
    """
    V1 Players API for retrieving player statistics.

    Example:
        >>> players_api.get(player_code="PDEL", season_code="E2024")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Players API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "v1/players")

    def get(
        self,
        player_code: str,
        season_code: str,
    ) -> dict[str, Any]:
        """Get player with accumulated stats per season and phase.

        Args:
            player_code: Player code/identifier
            season_code: Season code (e.g., 'E2024')

        Returns:
            Player information with accumulated statistics
        """
        return self._get(params={"playerCode": player_code, "seasonCode": season_code})

    async def get_async(
        self,
        player_code: str,
        season_code: str,
    ) -> dict[str, Any]:
        """Get player with accumulated stats per season and phase (async).

        Args:
            player_code: Player code/identifier
            season_code: Season code (e.g., 'E2024')

        Returns:
            Player information with accumulated statistics
        """
        return await self._get_async(
            params={"playerCode": player_code, "seasonCode": season_code}
        )
