"""V2 Competitions API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class CompetitionsAPI(BaseAPI):
    """
    V2 Competitions API for retrieving competition information.

    Example:
        >>> competitions_api.list()
        >>> competitions_api.get("E")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Competitions API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get all competitions.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of competitions
        """
        return self._get(
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            }
        )

    async def list_async(
        self,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get all competitions (async)."""
        return await self._get_async(
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            }
        )

    def get(self, competition_code: str) -> dict[str, Any]:
        """Get competition by code.

        Args:
            competition_code: Competition code (e.g., 'E' for Euroleague)

        Returns:
            Competition details
        """
        return self._get(competition_code)

    async def get_async(self, competition_code: str) -> dict[str, Any]:
        """Get competition by code (async)."""
        return await self._get_async(competition_code)
