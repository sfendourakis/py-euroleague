"""V3 Team Statistics API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class TeamStatsAPI(BaseAPI):
    """
    V3 Team Statistics API for retrieving detailed team statistics.

    Provides access to leaders, traditional stats, advanced stats,
    and opponent statistics.

    Example:
        >>> team_stats_api.leaders("E")
        >>> team_stats_api.traditional("E", season_code="2024")
        >>> team_stats_api.opponents_traditional("E", season_code="2024")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Team Stats API."""
        super().__init__(http_client, "v3/competitions")

    def leaders(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        from_season_code: Optional[str] = None,
        to_season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get team leaders statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code for single mode
            from_season_code: Start season for range mode
            to_season_code: End season for range mode
            phase_type_code: Phase type filter
            limit: Maximum number of results

        Returns:
            Team leaders statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "teams",
            "leaders",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "limit": limit,
            },
        )

    async def leaders_async(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        from_season_code: Optional[str] = None,
        to_season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get team leaders statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "teams",
            "leaders",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "limit": limit,
            },
        )

    def traditional(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get traditional team statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Traditional team statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "teams",
            "traditional",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )

    async def traditional_async(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get traditional team statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "teams",
            "traditional",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )

    def advanced(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get advanced team statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Advanced team statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "teams",
            "advanced",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )

    async def advanced_async(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get advanced team statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "teams",
            "advanced",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )

    def opponents_traditional(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get traditional opponent statistics (defensive stats).

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Traditional opponent statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "teams",
            "opponentsTraditional",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )

    async def opponents_traditional_async(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get traditional opponent statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "teams",
            "opponentsTraditional",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )

    def opponents_advanced(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get advanced opponent statistics (defensive stats).

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Advanced opponent statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "teams",
            "opponentsAdvanced",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )

    async def opponents_advanced_async(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        statistic_mode: Optional[str] = None,
        statistic: Optional[str] = None,
        sort_direction: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> dict[str, Any]:
        """Get advanced opponent statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "teams",
            "opponentsAdvanced",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "phaseTypeCode": phase_type_code,
                "statisticMode": statistic_mode,
                "statistic": statistic,
                "sortDirection": sort_direction,
                "offset": offset,
                "limit": limit,
            },
        )
