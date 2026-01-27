"""V2 Season Clubs API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class SeasonClubsAPI(BaseAPI):
    """
    V2 Season Clubs API for retrieving season-specific club information.

    Example:
        >>> season_clubs_api.list("E", "2024")
        >>> season_clubs_api.get("E", "2024", "BAR")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Season Clubs API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        competition_code: str,
        season_code: str,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get clubs for a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of season clubs
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def list_async(
        self,
        competition_code: str,
        season_code: str,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get clubs for a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    def get(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
    ) -> dict[str, Any]:
        """Get specific season club.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            club_code: Club code (e.g., 'BAR')

        Returns:
            Season club details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
        )

    async def get_async(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
    ) -> dict[str, Any]:
        """Get specific season club (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
        )

    def get_club_seasons(
        self,
        competition_code: str,
        club_code: str,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get all seasons for a club.

        Args:
            competition_code: Competition code (e.g., 'E')
            club_code: Club code (e.g., 'BAR')
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Paginated list of seasons for the club
        """
        return self._get(
            competition_code,
            "clubs",
            club_code,
            "seasons",
            params={
                "Limit": limit,
                "Offset": offset,
            },
        )

    async def get_club_seasons_async(
        self,
        competition_code: str,
        club_code: str,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get all seasons for a club (async)."""
        return await self._get_async(
            competition_code,
            "clubs",
            club_code,
            "seasons",
            params={
                "Limit": limit,
                "Offset": offset,
            },
        )
