"""V2 Season People API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class SeasonPeopleAPI(BaseAPI):
    """
    V2 Season People API for retrieving season-specific people information.

    Example:
        >>> season_people_api.list("E", "2024")
        >>> season_people_api.get("E", "2024", "PDEL")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Season People API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        competition_code: str,
        season_code: str,
        person_type: str | None = None,
        active: bool | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        sort_by: str | None = None,
    ) -> dict[str, Any]:
        """Get people for a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            person_type: Optional person type filter (e.g., 'Player', 'Coach')
            active: Optional active status filter
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering
            sort_by: Sort field

        Returns:
            Paginated list of season people
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "people",
            params={
                "personType": person_type,
                "active": active,
                "Limit": limit,
                "Offset": offset,
                "search": search,
                "sortBy": sort_by,
            },
        )

    async def list_async(
        self,
        competition_code: str,
        season_code: str,
        person_type: str | None = None,
        active: bool | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
        sort_by: str | None = None,
    ) -> dict[str, Any]:
        """Get people for a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "people",
            params={
                "personType": person_type,
                "active": active,
                "Limit": limit,
                "Offset": offset,
                "search": search,
                "sortBy": sort_by,
            },
        )

    def get(
        self,
        competition_code: str,
        season_code: str,
        person_code: str,
        active: bool | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get specific season person.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            person_code: Person code
            active: Optional active status filter
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Season person details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "people",
            person_code,
            params={
                "active": active,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def get_async(
        self,
        competition_code: str,
        season_code: str,
        person_code: str,
        active: bool | None = None,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get specific season person (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "people",
            person_code,
            params={
                "active": active,
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    def get_by_external_id(
        self,
        competition_code: str,
        season_code: str,
        external_id: str,
    ) -> dict[str, Any]:
        """Get season person by external ID.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            external_id: External ID

        Returns:
            Season person details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "people",
            external_id,
            "person",
        )

    async def get_by_external_id_async(
        self,
        competition_code: str,
        season_code: str,
        external_id: str,
    ) -> dict[str, Any]:
        """Get season person by external ID (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "people",
            external_id,
            "person",
        )

    def list_by_club(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        active: bool | None = None,
        person_type: str | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get people for a specific club in a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            club_code: Club code (e.g., 'BAR')
            active: Optional active status filter
            person_type: Optional person type filter
            search: Search string for filtering

        Returns:
            List of club season people
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "people",
            params={
                "active": active,
                "personType": person_type,
                "search": search,
            },
        )

    async def list_by_club_async(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        active: bool | None = None,
        person_type: str | None = None,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get people for a specific club in a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "people",
            params={
                "active": active,
                "personType": person_type,
                "search": search,
            },
        )

    def get_club_person(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        person_code: str,
    ) -> dict[str, Any]:
        """Get specific person for a club in a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            club_code: Club code (e.g., 'BAR')
            person_code: Person code

        Returns:
            Club season person details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "people",
            person_code,
        )

    async def get_club_person_async(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        person_code: str,
    ) -> dict[str, Any]:
        """Get specific person for a club in a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "people",
            person_code,
        )

    def get_competition_players(
        self,
        competition_code: str,
        season_code: str | None = None,
        search: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get competition players.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Optional season code filter
            search: Search string for filtering
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            Paginated list of competition players
        """
        return self._get(
            competition_code,
            "players",
            params={
                "seasonCode": season_code,
                "search": search,
                "Limit": limit,
                "Offset": offset,
            },
        )

    async def get_competition_players_async(
        self,
        competition_code: str,
        season_code: str | None = None,
        search: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict[str, Any]:
        """Get competition players (async)."""
        return await self._get_async(
            competition_code,
            "players",
            params={
                "seasonCode": season_code,
                "search": search,
                "Limit": limit,
                "Offset": offset,
            },
        )
