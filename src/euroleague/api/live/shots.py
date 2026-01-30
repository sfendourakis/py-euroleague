"""Shots API endpoint for shot location data."""

from typing import Any

from euroleague.api.base import BaseAPI
from euroleague.models.live.shots import ShotsResponse


class ShotsAPI(BaseAPI):
    """API for retrieving shot location data with coordinates.

    Provides access to detailed shot data for Euroleague games,
    including coordinates for shot chart visualization, shooting zones,
    and contextual information like fastbreak and second-chance plays.

    Example:
        >>> with EuroleagueClient() as client:
        ...     shots = client.live.shots.get("E2025", 241)
        ...     for shot in shots.field_goals:
        ...         if shot.has_coordinates:
        ...             print(f"{shot.player}: ({shot.coord_x}, {shot.coord_y})")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize the Shots API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "")

    def get(self, season_code: str, game_code: int) -> ShotsResponse:
        """Get shot data with coordinates for a game.

        Args:
            season_code: Season code (e.g., 'E2025' for Euroleague 2024-25)
            game_code: Game code/number

        Returns:
            ShotsResponse with all shots and their coordinates

        Example:
            >>> shots = client.live.shots.get("E2025", 241)
            >>> print(f"Total shots: {shots.total_shots}")
            >>> print(f"FG%: {shots.get_field_goal_percentage():.1f}%")
        """
        data = self._get(
            "Points",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )
        return ShotsResponse.model_validate(data)

    async def get_async(self, season_code: str, game_code: int) -> ShotsResponse:
        """Get shot data with coordinates for a game (async).

        Args:
            season_code: Season code (e.g., 'E2025' for Euroleague 2024-25)
            game_code: Game code/number

        Returns:
            ShotsResponse with all shots and their coordinates
        """
        data = await self._get_async(
            "Points",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )
        return ShotsResponse.model_validate(data)

    def get_raw(self, season_code: str, game_code: int) -> dict[str, Any]:
        """Get raw shot data without model parsing.

        Useful for debugging or accessing fields not in the model.

        Args:
            season_code: Season code (e.g., 'E2025')
            game_code: Game code/number

        Returns:
            Raw JSON response as dictionary
        """
        return self._get(
            "Points",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )

    async def get_raw_async(self, season_code: str, game_code: int) -> dict[str, Any]:
        """Get raw shot data without model parsing (async).

        Args:
            season_code: Season code (e.g., 'E2025')
            game_code: Game code/number

        Returns:
            Raw JSON response as dictionary
        """
        return await self._get_async(
            "Points",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )
