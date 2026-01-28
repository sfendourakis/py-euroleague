"""V2 Stats API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class StatsAPI(BaseAPI):
    """
    V2 Stats API for retrieving statistical information.

    Example:
        >>> stats_api.get_club_highs("E", "BAR")
        >>> stats_api.get_club_leaders("E")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Stats API."""
        super().__init__(http_client, "v2/competitions")

    def get_club_highs(
        self,
        competition_code: str,
        club_code: str,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club high statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            club_code: Club code (e.g., 'BAR')
            season_mode: Season mode (Single/Range)
            season_code: Season code for single mode
            from_season_code: Start season for range mode
            to_season_code: End season for range mode
            phase_type_code: Phase type filter
            category: Statistic category
            aggregate: Aggregation type
            misc: Miscellaneous filter
            limit: Maximum number of results

        Returns:
            Club high statistics
        """
        return self._get(
            competition_code,
            "stats",
            "clubs",
            club_code,
            "highs",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    async def get_club_highs_async(
        self,
        competition_code: str,
        club_code: str,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club high statistics (async)."""
        return await self._get_async(
            competition_code,
            "stats",
            "clubs",
            club_code,
            "highs",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    def get_club_lows(
        self,
        competition_code: str,
        club_code: str,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club low statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            club_code: Club code (e.g., 'BAR')
            season_mode: Season mode (Single/Range)
            season_code: Season code for single mode
            from_season_code: Start season for range mode
            to_season_code: End season for range mode
            phase_type_code: Phase type filter
            category: Statistic category
            aggregate: Aggregation type
            misc: Miscellaneous filter
            limit: Maximum number of results

        Returns:
            Club low statistics
        """
        return self._get(
            competition_code,
            "stats",
            "clubs",
            club_code,
            "lows",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    async def get_club_lows_async(
        self,
        competition_code: str,
        club_code: str,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club low statistics (async)."""
        return await self._get_async(
            competition_code,
            "stats",
            "clubs",
            club_code,
            "lows",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    def get_club_leaders(
        self,
        competition_code: str,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club leaders statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_mode: Season mode (Single/Range)
            season_code: Season code for single mode
            from_season_code: Start season for range mode
            to_season_code: End season for range mode
            phase_type_code: Phase type filter
            category: Statistic category
            aggregate: Aggregation type
            misc: Miscellaneous filter
            limit: Maximum number of results

        Returns:
            Club leaders statistics
        """
        return self._get(
            competition_code,
            "stats",
            "clubs",
            "leaders",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    async def get_club_leaders_async(
        self,
        competition_code: str,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club leaders statistics (async)."""
        return await self._get_async(
            competition_code,
            "stats",
            "clubs",
            "leaders",
            params={
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    def get_club_records(
        self,
        competition_code: str,
        group_by: str | None = None,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club record statistics.

        Args:
            competition_code: Competition code (e.g., 'E')
            group_by: Grouping field
            season_mode: Season mode (Single/Range)
            season_code: Season code for single mode
            from_season_code: Start season for range mode
            to_season_code: End season for range mode
            phase_type_code: Phase type filter
            category: Statistic category
            aggregate: Aggregation type
            misc: Miscellaneous filter
            limit: Maximum number of results

        Returns:
            Club record statistics
        """
        return self._get(
            competition_code,
            "stats",
            "clubs",
            "records",
            params={
                "groupBy": group_by,
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )

    async def get_club_records_async(
        self,
        competition_code: str,
        group_by: str | None = None,
        season_mode: str | None = None,
        season_code: str | None = None,
        from_season_code: str | None = None,
        to_season_code: str | None = None,
        phase_type_code: str | None = None,
        category: str | None = None,
        aggregate: str | None = None,
        misc: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Get club record statistics (async)."""
        return await self._get_async(
            competition_code,
            "stats",
            "clubs",
            "records",
            params={
                "groupBy": group_by,
                "SeasonMode": season_mode,
                "SeasonCode": season_code,
                "FromSeasonCode": from_season_code,
                "ToSeasonCode": to_season_code,
                "phaseTypeCode": phase_type_code,
                "category": category,
                "aggregate": aggregate,
                "misc": misc,
                "limit": limit,
            },
        )
