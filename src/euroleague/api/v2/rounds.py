"""V2 Rounds API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class RoundsAPI(BaseAPI):
    """
    V2 Rounds API for retrieving round information.

    Example:
        >>> rounds_api.list("E", "2024")
        >>> rounds_api.get("E", "2024", 10)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Rounds API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get rounds for a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            phase_type_code: Optional phase type filter
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of rounds
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            params={
                "phaseTypeCode": phase_type_code,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def list_async(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get rounds for a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            params={
                "phaseTypeCode": phase_type_code,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    def get(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get specific round.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number

        Returns:
            Round details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
        )

    async def get_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get specific round (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
        )
