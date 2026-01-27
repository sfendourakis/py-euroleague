"""V2 Phases API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class PhasesAPI(BaseAPI):
    """
    V2 Phases API for retrieving phase information.

    Example:
        >>> phases_api.list("E", "2024")
        >>> phases_api.get("E", "2024", "RS")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Phases API."""
        super().__init__(http_client, "v2/competitions")

    def list(
        self,
        competition_code: str,
        season_code: str,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get phases for a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            search: Search string for filtering

        Returns:
            List of phases
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "phases",
            params={"search": search},
        )

    async def list_async(
        self,
        competition_code: str,
        season_code: str,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get phases for a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "phases",
            params={"search": search},
        )

    def get(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str,
    ) -> dict[str, Any]:
        """Get specific phase.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            phase_type_code: Phase type code (e.g., 'RS')

        Returns:
            Phase details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
        )

    async def get_async(
        self,
        competition_code: str,
        season_code: str,
        phase_type_code: str,
    ) -> dict[str, Any]:
        """Get specific phase (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "phases",
            phase_type_code,
        )

    def list_for_club(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get phases for a specific club in a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            club_code: Club code (e.g., 'BAR')
            search: Search string for filtering

        Returns:
            List of phases
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "phases",
            params={"search": search},
        )

    async def list_for_club_async(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get phases for a specific club in a season (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "phases",
            params={"search": search},
        )
