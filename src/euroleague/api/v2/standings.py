"""V2 Standings API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class StandingsAPI(BaseAPI):
    """
    V2 Standings API for retrieving standings information.

    Example:
        >>> standings_api.get_round("E", "2024", 10)
        >>> standings_api.get_group("E", "2024", 10, 1)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Standings API."""
        super().__init__(http_client, "v2/competitions")

    def get_round(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get standings for a round.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number

        Returns:
            Round standings
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "standings",
        )

    async def get_round_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get standings for a round (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "standings",
        )

    def get_group(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
        group_id: int,
    ) -> dict[str, Any]:
        """Get standings for a specific group.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number
            group_id: Group ID

        Returns:
            Group standings
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "groups",
            str(group_id),
            "standings",
        )

    async def get_group_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
        group_id: int,
    ) -> dict[str, Any]:
        """Get standings for a specific group (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "groups",
            str(group_id),
            "standings",
        )

    def get_standing_entry(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
        group_id: int,
        standing_id: int,
    ) -> dict[str, Any]:
        """Get a single standing entry.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number
            group_id: Group ID
            standing_id: Standing ID

        Returns:
            Standing entry details
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "groups",
            str(group_id),
            "standings",
            str(standing_id),
        )

    async def get_standing_entry_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
        group_id: int,
        standing_id: int,
    ) -> dict[str, Any]:
        """Get a single standing entry (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "groups",
            str(group_id),
            "standings",
            str(standing_id),
        )
