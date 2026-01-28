"""V2 Records API endpoint."""

from typing import Any

from euroleague.api.base import BaseAPI


class RecordsAPI(BaseAPI):
    """
    V2 Records API for retrieving historical records.

    Example:
        >>> records_api.get_club_game_records("BAR", "E")
        >>> records_api.get_player_career_highs("E", "PDEL")
    """

    def __init__(self, http_client: Any) -> None:
        """Initialize Records API."""
        super().__init__(http_client, "v2")

    def get_club_game_records(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get club highest single-game results.

        Args:
            club_code: Club code (e.g., 'BAR')
            competition_code: Competition code (e.g., 'E')

        Returns:
            Club game records
        """
        return self._get(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "gamerecords",
        )

    async def get_club_game_records_async(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get club highest single-game results (async)."""
        return await self._get_async(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "gamerecords",
        )

    def get_club_season_records(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get club season averages.

        Args:
            club_code: Club code (e.g., 'BAR')
            competition_code: Competition code (e.g., 'E')

        Returns:
            Club season records
        """
        return self._get(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "seasonrecords",
        )

    async def get_club_season_records_async(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get club season averages (async)."""
        return await self._get_async(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "seasonrecords",
        )

    def get_player_highs(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get team player single-game highs.

        Args:
            club_code: Club code (e.g., 'BAR')
            competition_code: Competition code (e.g., 'E')

        Returns:
            Player highs for the club
        """
        return self._get(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "playerhighs",
        )

    async def get_player_highs_async(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get team player single-game highs (async)."""
        return await self._get_async(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "playerhighs",
        )

    def get_player_season_records(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get team player season averages.

        Args:
            club_code: Club code (e.g., 'BAR')
            competition_code: Competition code (e.g., 'E')

        Returns:
            Player season records for the club
        """
        return self._get(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "playerseasonrecords",
        )

    async def get_player_season_records_async(
        self,
        club_code: str,
        competition_code: str,
    ) -> dict[str, Any]:
        """Get team player season averages (async)."""
        return await self._get_async(
            "clubs",
            club_code,
            "competition",
            competition_code,
            "playerseasonrecords",
        )

    def get_player_career_highs(
        self,
        competition_code: str,
        person_code: str,
        phase_type_code: str | None = None,
    ) -> dict[str, Any]:
        """Get player career highs.

        Args:
            competition_code: Competition code (e.g., 'E')
            person_code: Person code
            phase_type_code: Optional phase type filter

        Returns:
            Player career highs
        """
        return self._get(
            "competitions",
            competition_code,
            "people",
            person_code,
            "careerhighs",
            params={"phaseTypeCode": phase_type_code},
        )

    async def get_player_career_highs_async(
        self,
        competition_code: str,
        person_code: str,
        phase_type_code: str | None = None,
    ) -> dict[str, Any]:
        """Get player career highs (async)."""
        return await self._get_async(
            "competitions",
            competition_code,
            "people",
            person_code,
            "careerhighs",
            params={"phaseTypeCode": phase_type_code},
        )

    def get_player_season_ranks(
        self,
        competition_code: str,
        season_code: str,
        person_code: str,
    ) -> dict[str, Any]:
        """Get player season rankings.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            person_code: Person code

        Returns:
            Player season rankings
        """
        return self._get(
            "competitions",
            competition_code,
            "seasons",
            season_code,
            "people",
            person_code,
            "ranks",
        )

    async def get_player_season_ranks_async(
        self,
        competition_code: str,
        season_code: str,
        person_code: str,
    ) -> dict[str, Any]:
        """Get player season rankings (async)."""
        return await self._get_async(
            "competitions",
            competition_code,
            "seasons",
            season_code,
            "people",
            person_code,
            "ranks",
        )

    def get_person_game_records(
        self,
        competition_code: str,
        person_code: str,
        person_type: str | None = None,
        club_code: str | None = None,
        versus_club_code: str | None = None,
        versus_person_code: str | None = None,
        versus_person_type: str | None = None,
        phase_type_code: str | None = None,
    ) -> dict[str, Any]:
        """Get person game records.

        Args:
            competition_code: Competition code (e.g., 'E')
            person_code: Person code
            person_type: Optional person type filter
            club_code: Optional club code filter
            versus_club_code: Optional versus club code filter
            versus_person_code: Optional versus person code filter
            versus_person_type: Optional versus person type filter
            phase_type_code: Optional phase type filter

        Returns:
            Person game records
        """
        return self._get(
            "competitions",
            competition_code,
            "people",
            person_code,
            "records",
            params={
                "personType": person_type,
                "clubCode": club_code,
                "versusClubCode": versus_club_code,
                "versusPersonCode": versus_person_code,
                "versusPersonType": versus_person_type,
                "phaseTypeCode": phase_type_code,
            },
        )

    async def get_person_game_records_async(
        self,
        competition_code: str,
        person_code: str,
        person_type: str | None = None,
        club_code: str | None = None,
        versus_club_code: str | None = None,
        versus_person_code: str | None = None,
        versus_person_type: str | None = None,
        phase_type_code: str | None = None,
    ) -> dict[str, Any]:
        """Get person game records (async)."""
        return await self._get_async(
            "competitions",
            competition_code,
            "people",
            person_code,
            "records",
            params={
                "personType": person_type,
                "clubCode": club_code,
                "versusClubCode": versus_club_code,
                "versusPersonCode": versus_person_code,
                "versusPersonType": versus_person_type,
                "phaseTypeCode": phase_type_code,
            },
        )

    def get_club_win_loss(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
    ) -> dict[str, Any]:
        """Get club win-loss ratio for a season.

        Args:
            competition_code: Competition code (e.g., 'E')
            season_code: Season code (e.g., '2024')
            club_code: Club code (e.g., 'BAR')

        Returns:
            Club win-loss records
        """
        return self._get(
            "competitions",
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "records",
        )

    async def get_club_win_loss_async(
        self,
        competition_code: str,
        season_code: str,
        club_code: str,
    ) -> dict[str, Any]:
        """Get club win-loss ratio for a season (async)."""
        return await self._get_async(
            "competitions",
            competition_code,
            "seasons",
            season_code,
            "clubs",
            club_code,
            "records",
        )
