"""V3 Coaches API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class CoachesAPI(BaseAPI):
    """
    V3 Coaches API for retrieving coach records.

    Example:
        >>> coaches_api.get_records("E", "2024", "COACH001")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Coaches API."""
        super().__init__(http_client, "v3/competitions")

    def get_records(
        self,
        competition_code: str,
        season_code: str,
        coach_code: str,
    ) -> dict[str, Any]:
        """Get coach records.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            coach_code: Coach code

        Returns:
            Coach records
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "coaches",
            coach_code,
        )

    async def get_records_async(
        self,
        competition_code: str,
        season_code: str,
        coach_code: str,
    ) -> dict[str, Any]:
        """Get coach records (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "coaches",
            coach_code,
        )
