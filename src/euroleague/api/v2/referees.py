"""V2 Referees API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class RefereesAPI(BaseAPI):
    """
    V2 Referees API for retrieving referee information.

    Example:
        >>> referees_api.list()
        >>> referees_api.get("REF001")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Referees API."""
        super().__init__(http_client, "v2/referees")

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get all registered referees.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of referees
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
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get all registered referees (async)."""
        return await self._get_async(
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            }
        )

    def get(self, person_code: str) -> dict[str, Any]:
        """Get referee by person code.

        Args:
            person_code: Person code

        Returns:
            Referee details
        """
        return self._get(person_code)

    async def get_async(self, person_code: str) -> dict[str, Any]:
        """Get referee by person code (async)."""
        return await self._get_async(person_code)

    def list_by_competition(
        self,
        competition_code: str,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get referees for a competition.

        Args:
            competition_code: Competition code (e.g., 'E')
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of referees
        """
        # Need to use a different base path for this endpoint
        path = f"v2/competitions/{competition_code}/referees"
        return self._http.get(  # type: ignore[return-value]
            path,
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def list_by_competition_async(
        self,
        competition_code: str,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get referees for a competition (async)."""
        path = f"v2/competitions/{competition_code}/referees"
        return await self._http.get(  # type: ignore[misc,no-any-return]
            path,
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    def list_by_season(
        self,
        competition_code: str,
        season_code: str,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get referees for a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of referees
        """
        path = f"v2/competitions/{competition_code}/seasons/{season_code}/referees"
        return self._http.get(  # type: ignore[return-value]
            path,
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def list_by_season_async(
        self,
        competition_code: str,
        season_code: str,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get referees for a season (async)."""
        path = f"v2/competitions/{competition_code}/seasons/{season_code}/referees"
        return await self._http.get(  # type: ignore[misc,no-any-return]
            path,
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )
