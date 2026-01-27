"""V2 Clubs API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class ClubsAPI(BaseAPI):
    """
    V2 Clubs API for retrieving club information.

    Example:
        >>> clubs_api.list()
        >>> clubs_api.get("BAR")
        >>> clubs_api.get_info("BAR")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Clubs API."""
        super().__init__(http_client, "v2/clubs")

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        has_parent_club: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get all registered clubs.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            has_parent_club: Filter by parent club status
            search: Search string for filtering

        Returns:
            Paginated list of clubs
        """
        return self._get(
            params={
                "Limit": limit,
                "Offset": offset,
                "hasParentClub": has_parent_club,
                "search": search,
            }
        )

    async def list_async(
        self,
        limit: int = 20,
        offset: int = 0,
        has_parent_club: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get all registered clubs (async)."""
        return await self._get_async(
            params={
                "Limit": limit,
                "Offset": offset,
                "hasParentClub": has_parent_club,
                "search": search,
            }
        )

    def get(self, club_code: str) -> dict[str, Any]:
        """Get specific club by code.

        Args:
            club_code: Club code (e.g., 'BAR')

        Returns:
            Club details
        """
        return self._get(club_code)

    async def get_async(self, club_code: str) -> dict[str, Any]:
        """Get specific club by code (async)."""
        return await self._get_async(club_code)

    def get_info(self, club_code: str) -> dict[str, Any]:
        """Get club information.

        Args:
            club_code: Club code (e.g., 'BAR')

        Returns:
            Club information
        """
        return self._get(club_code, "info")

    async def get_info_async(self, club_code: str) -> dict[str, Any]:
        """Get club information (async)."""
        return await self._get_async(club_code, "info")

    def get_videos(self, club_code: str) -> dict[str, Any]:
        """Get latest club videos.

        Args:
            club_code: Club code (e.g., 'BAR')

        Returns:
            Club videos
        """
        return self._get(club_code, "videos")

    async def get_videos_async(self, club_code: str) -> dict[str, Any]:
        """Get latest club videos (async)."""
        return await self._get_async(club_code, "videos")
