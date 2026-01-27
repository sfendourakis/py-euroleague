"""V3 Player Statistics API endpoint."""

from typing import Any, Optional

from euroleague.api.base import BaseAPI


class PlayerStatsAPI(BaseAPI):
    """
    V3 Player Statistics API for retrieving detailed player statistics.

    Provides access to leaders, traditional stats, advanced stats,
    miscellaneous stats, and scoring stats.

    Example:
        >>> player_stats_api.leaders("E")
        >>> player_stats_api.traditional("E", season_code="2024")
        >>> player_stats_api.advanced("E", season_code="2024")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Player Stats API."""
        super().__init__(http_client, "v3/competitions")

    def leaders(
        self,
        competition_code: str,
        season_mode: Optional[str] = None,
        season_code: Optional[str] = None,
        from_season_code: Optional[str] = None,
        to_season_code: Optional[str] = None,
        phase_type_code: Optional[str] = None,
        team_code: Optional[str] = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get player leaders statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code for single mode
            from_season_code: Start season for range mode
            to_season_code: End season for range mode
            phase_type_code: Phase type filter
            team_code: Team code filter
            limit: Maximum number of results

        Returns:
            Player leaders statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "players",
            "leaders",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "teamCode": team_code,
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
        team_code: Optional[str] = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get player leaders statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "players",
            "leaders",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "teamCode": team_code,
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
        """Get traditional player statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated/Per40)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Traditional player statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "players",
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
        """Get traditional player statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "players",
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
        """Get advanced player statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated/Per40)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Advanced player statistics (PER, TS%, usage rate, etc.)
        """
        return self._get(
            competition_code,
            "statistics",
            "players",
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
        """Get advanced player statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "players",
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

    def misc(
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
        """Get miscellaneous player statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated/Per40)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Miscellaneous player statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "players",
            "misc",
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

    async def misc_async(
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
        """Get miscellaneous player statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "players",
            "misc",
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

    def scoring(
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
        """Get scoring player statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code
            phase_type_code: Phase type filter
            statistic_mode: Statistic mode (PerGame/Accumulated/Per40)
            statistic: Specific statistic to sort by
            sort_direction: Sort direction (Ascending/Descending)
            offset: Number of results to skip
            limit: Maximum number of results

        Returns:
            Scoring player statistics
        """
        return self._get(
            competition_code,
            "statistics",
            "players",
            "scoring",
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

    async def scoring_async(
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
        """Get scoring player statistics (async)."""
        return await self._get_async(
            competition_code,
            "statistics",
            "players",
            "scoring",
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
