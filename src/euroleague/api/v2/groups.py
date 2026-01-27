"""V2 Groups API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class GroupsAPI(BaseAPI):
    """
    V2 Groups API for retrieving group information within phases.

    Example:
        >>> groups_api.list("E", "2024", "RS")
        >>> groups_api.get("E", "2024", "RS", 1)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Groups API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get groups for a phase.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            phase_type_code: Phase type code (e.g., 'RS')
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of groups
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
            "groups",
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
        phase_type_code: str,
        limit: int = 20,
        offset: int = 0,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get groups for a phase (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
            "groups",
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
        phase_type_code: str,
        group_id: int,
    ) -> dict[str, Any]:
        """Get specific group by ID.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            phase_type_code: Phase type code (e.g., 'RS')
            group_id: Group ID

        Returns:
            Group details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
            "groups",
            str(group_id),
        )

    async def get_async(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str,
        group_id: int,
    ) -> dict[str, Any]:
        """Get specific group by ID (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
            "groups",
            str(group_id),
        )

    def get_by_name(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str,
        group_name: str,
    ) -> dict[str, Any]:
        """Get group by name.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            phase_type_code: Phase type code (e.g., 'RS')
            group_name: Group raw name

        Returns:
            Group details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
            "groups",
            "name",
            group_name,
        )

    async def get_by_name_async(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str,
        group_name: str,
    ) -> dict[str, Any]:
        """Get group by name (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
            "groups",
            "name",
            group_name,
        )
