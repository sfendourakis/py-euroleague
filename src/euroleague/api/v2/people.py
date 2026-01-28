"""V2 People API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class PeopleAPI(BaseAPI):
    """
    V2 People API for retrieving person information (players, coaches, etc).

    Example:
        >>> people_api.list()
        >>> people_api.get("PDEL")
        >>> people_api.get_bio("PDEL")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize People API."""
        super().__init__(http_client, "v2/people")

    def list(
        self,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get all registered people.

        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of people
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
        """Get all registered people (async)."""
        return await self._get_async(
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            }
        )

    def get(self, person_code: str) -> dict[str, Any]:
        """Get person by code.

        Args:
            person_code: Person code

        Returns:
            Person details
        """
        return self._get(person_code)

    async def get_async(self, person_code: str) -> dict[str, Any]:
        """Get person by code (async)."""
        return await self._get_async(person_code)

    def get_bio(self, person_code: str) -> dict[str, Any]:
        """Get person biography.

        Args:
            person_code: Person code

        Returns:
            Person biography
        """
        return self._get(person_code, "bio")

    async def get_bio_async(self, person_code: str) -> dict[str, Any]:
        """Get person biography (async)."""
        return await self._get_async(person_code, "bio")

    def get_seasons(
        self,
        person_code: str,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get person's seasons.

        Args:
            person_code: Person code
            limit: Maximum number of results
            offset: Number of results to skip
            search: Search string for filtering

        Returns:
            Paginated list of seasons
        """
        return self._get(
            person_code,
            "seasons",
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )

    async def get_seasons_async(
        self,
        person_code: str,
        limit: int = 20,
        offset: int = 0,
        search: str | None = None,
    ) -> dict[str, Any]:
        """Get person's seasons (async)."""
        return await self._get_async(
            person_code,
            "seasons",
            params={
                "Limit": limit,
                "Offset": offset,
                "search": search,
            },
        )
