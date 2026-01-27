"""V1 Games API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class GamesAPI(BaseAPI):
    """
    V1 Games API for retrieving box score information.

    Example:
        >>> games_api.get(season_code="E2024", game_code=1)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Games API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "v1/games")

    def get(
        self,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get box score information for a specific game.

        Args:
            season_code: Season code (e.g., 'E2024')
            game_code: Game code/number

        Returns:
            Box score data including team stats, player stats, and game info
        """
        return self._get(params={"seasonCode": season_code, "gameCode": game_code})

    async def get_async(
        self,
        season_code: str,
        game_code: int,
    ) -> dict[str, Any]:
        """Get box score information for a specific game (async).

        Args:
            season_code: Season code (e.g., 'E2024')
            game_code: Game code/number

        Returns:
            Box score data including team stats, player stats, and game info
        """
        return await self._get_async(params={"seasonCode": season_code, "gameCode": game_code})
