"""Play-by-play API endpoint for live game data."""

from typing import Any

from euroleague.api.base import BaseAPI
from euroleague.models.live.play_by_play import PlayByPlayResponse


class PlayByPlayAPI(BaseAPI):
    """API for retrieving play-by-play game data.

    Provides access to detailed play-by-play information for Euroleague games,
    including all events (shots, rebounds, assists, turnovers, fouls, etc.)
    with timestamps and score progression.

    Example:
        >>> with EuroleagueClient() as client:
        ...     pbp = client.live.play_by_play.get("E2025", 241)
        ...     for play in pbp.first_quarter:
        ...         print(f"{play.marker_time} - {play.player}: {play.play_info}")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize the PlayByPlay API.

        Args:
            http_client: HTTP client for making requests
        """
        super().__init__(http_client, "")

    def get(self, season_code: str, game_code: int) -> PlayByPlayResponse:
        """Get play-by-play data for a game.

        Args:
            season_code: Season code (e.g., 'E2025' for Euroleague 2024-25)
            game_code: Game code/number

        Returns:
            PlayByPlayResponse with all plays organized by quarter

        Example:
            >>> pbp = client.live.play_by_play.get("E2025", 241)
            >>> print(f"Total plays: {pbp.total_plays}")
            >>> for play in pbp.get_scoring_plays():
            ...     print(f"{play.player} scored {play.points_scored} points")
        """
        data = self._get(
            "PlayByPlay",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )
        return PlayByPlayResponse.model_validate(data)

    async def get_async(self, season_code: str, game_code: int) -> PlayByPlayResponse:
        """Get play-by-play data for a game (async).

        Args:
            season_code: Season code (e.g., 'E2025' for Euroleague 2024-25)
            game_code: Game code/number

        Returns:
            PlayByPlayResponse with all plays organized by quarter
        """
        data = await self._get_async(
            "PlayByPlay",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )
        return PlayByPlayResponse.model_validate(data)

    def get_raw(self, season_code: str, game_code: int) -> dict[str, Any]:
        """Get raw play-by-play data without model parsing.

        Useful for debugging or accessing fields not in the model.

        Args:
            season_code: Season code (e.g., 'E2025')
            game_code: Game code/number

        Returns:
            Raw JSON response as dictionary
        """
        return self._get(
            "PlayByPlay",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )

    async def get_raw_async(self, season_code: str, game_code: int) -> dict[str, Any]:
        """Get raw play-by-play data without model parsing (async).

        Args:
            season_code: Season code (e.g., 'E2025')
            game_code: Game code/number

        Returns:
            Raw JSON response as dictionary
        """
        return await self._get_async(
            "PlayByPlay",
            params={
                "seasoncode": season_code,
                "gamecode": game_code,
            },
        )
