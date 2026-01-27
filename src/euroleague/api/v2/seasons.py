"""V2 Seasons API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class SeasonsAPI(BaseAPI):
    """
    V2 Seasons API for retrieving season information.

    Example:
        >>> seasons_api.list("E")
        >>> seasons_api.get("E", "2024")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Seasons API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        competition_code: str,
        competition_year: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get seasons for a competition.

        Args:
            competition_code: Competition code (e.g., 'E')
            competition_year: Optional year filter
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of seasons
        """
        return self._get(
            competition_code,
            "seasons",
            params={
                "competitionYear": competition_year,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def list_async(
        self,
        competition_code: str,
        competition_year: Optional[int] = None,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get seasons for a competition (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            params={
                "competitionYear": competition_year,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    def get(
        self,
        competition_code: str,
        season_code: str,
    ) -> dict[str, Any]:
        """Get specific season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')

        Returns:
            Season details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
        )

    async def get_async(
        self,
        competition_code: str,
        season_code: str,
    ) -> dict[str, Any]:
        """Get specific season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
        )
