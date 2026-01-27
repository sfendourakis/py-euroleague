"""V3 Standings API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class StandingsAPI(BaseAPI):
    """
    V3 Standings API for retrieving various standings views.

    Provides access to calendar standings, streaks, ahead/behind,
    margins, and basic standings.

    Example:
        >>> standings_api.basic("E", "2024", 10)
        >>> standings_api.streaks("E", "2024", 10)
        >>> standings_api.margins("E", "2024", 10)
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Standings API."""
        super().__init__(http_client, "v3/competitions")

    def calendar(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get calendar standings.

        Shows each team's results round by round.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number

        Returns:
            Calendar standings
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "calendarstandings",
        )

    async def calendar_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get calendar standings (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "calendarstandings",
        )

    def streaks(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get streak standings.

        Shows winning/losing streaks for each team.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number

        Returns:
            Streak standings
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "streaks",
        )

    async def streaks_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get streak standings (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "streaks",
        )

    def ahead_behind(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get ahead/behind standings.

        Shows games ahead/behind for each team relative to others.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number

        Returns:
            Ahead/Behind standings
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "aheadbehind",
        )

    async def ahead_behind_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get ahead/behind standings (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "aheadbehind",
        )

    def margins(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get margins standings.

        Shows point differentials and margins for each team.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number

        Returns:
            Margins standings
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "margins",
        )

    async def margins_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get margins standings (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "margins",
        )

    def basic(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get basic standings.

        Shows standard win-loss standings.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            round_number: Round number

        Returns:
            Basic standings
        """
        return self._get(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "basicstandings",
        )

    async def basic_async(
        self,
        competition_code: str,
        season_code: str,
        round_number: int,
    ) -> dict[str, Any]:
        """Get basic standings (async)."""
        return await self._get_async(
            competition_code,
            "seasons",
            season_code,
            "rounds",
            str(round_number),
            "basicstandings",
        )
