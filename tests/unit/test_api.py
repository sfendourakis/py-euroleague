"""Unit tests for API endpoint modules."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from euroleague.api.base import BaseAPI
from euroleague.api.v1.games import GamesAPI as V1GamesAPI
from euroleague.api.v2.clubs import ClubsAPI
from euroleague.api.v2.games import GamesAPI as V2GamesAPI
from euroleague.api.v2.seasons import SeasonsAPI
from euroleague.api.v3.player_stats import PlayerStatsAPI
from euroleague.api.v3.standings import StandingsAPI
from euroleague.api.v3.team_stats import TeamStatsAPI


class TestBaseAPI:
    """Tests for BaseAPI class."""

    def test_build_path_with_base(self):
        """Should build path with base path prefix."""
        mock_http = MagicMock()
        api = BaseAPI(mock_http, "v1/test")

        path = api._build_path("a", "b", "c")
        assert path == "v1/test/a/b/c"

    def test_build_path_without_base(self):
        """Should build path without base path."""
        mock_http = MagicMock()
        api = BaseAPI(mock_http, "")

        path = api._build_path("a", "b")
        assert path == "a/b"

    def test_build_path_strips_slashes(self):
        """Should strip leading/trailing slashes from parts."""
        mock_http = MagicMock()
        api = BaseAPI(mock_http, "/v1/test/")

        path = api._build_path("/a/", "/b/")
        assert path == "v1/test/a/b"

    def test_get_delegates_to_http(self):
        """Sync get should delegate to HTTP client."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"data": "test"}
        api = BaseAPI(mock_http, "v1/test")

        result = api._get("endpoint", params={"limit": 10})

        mock_http.get.assert_called_once_with("v1/test/endpoint", params={"limit": 10})
        assert result == {"data": "test"}

    @pytest.mark.asyncio
    async def test_get_async_delegates_to_http(self):
        """Async get should delegate to HTTP client."""
        mock_http = AsyncMock()
        mock_http.get.return_value = {"data": "test"}
        api = BaseAPI(mock_http, "v1/test")

        result = await api._get_async("endpoint", params={"limit": 10})

        mock_http.get.assert_called_once_with("v1/test/endpoint", params={"limit": 10})
        assert result == {"data": "test"}


class TestV1GamesAPI:
    """Tests for V1 Games API."""

    def test_get_builds_correct_params(self):
        """get() should build correct params."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"boxScore": {}}
        api = V1GamesAPI(mock_http)

        api.get(season_code="E2024", game_code=1)

        mock_http.get.assert_called_once()
        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v1/games"
        assert call_args[1]["params"] == {"seasonCode": "E2024", "gameCode": 1}

    @pytest.mark.asyncio
    async def test_get_async_works(self):
        """get_async() should work correctly."""
        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value={"boxScore": {}})
        api = V1GamesAPI(mock_http)

        result = await api.get_async(season_code="E2024", game_code=1)

        assert result == {"boxScore": {}}


class TestClubsAPI:
    """Tests for V2 Clubs API."""

    def test_list_with_defaults(self):
        """list() should use default params."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"data": [], "total": 0}
        api = ClubsAPI(mock_http)

        api.list()

        call_args = mock_http.get.call_args
        params = call_args[1]["params"]
        assert params["Limit"] == 20
        assert params["Offset"] == 0

    def test_list_with_custom_params(self):
        """list() should accept custom params."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"data": [], "total": 0}
        api = ClubsAPI(mock_http)

        api.list(limit=50, offset=10, has_parent_club=True, search="madrid")

        call_args = mock_http.get.call_args
        params = call_args[1]["params"]
        assert params["Limit"] == 50
        assert params["Offset"] == 10
        assert params["hasParentClub"] is True
        assert params["search"] == "madrid"

    def test_get_builds_correct_path(self):
        """get() should include club code in path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"code": "BAR"}
        api = ClubsAPI(mock_http)

        api.get("BAR")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v2/clubs/BAR"

    def test_get_info_builds_correct_path(self):
        """get_info() should include info in path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"info": {}}
        api = ClubsAPI(mock_http)

        api.get_info("BAR")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v2/clubs/BAR/info"

    @pytest.mark.asyncio
    async def test_all_async_methods_exist(self):
        """All sync methods should have async counterparts."""
        sync_methods = ["list", "get", "get_info", "get_videos"]
        for method in sync_methods:
            async_method = f"{method}_async"
            assert hasattr(ClubsAPI, async_method), f"Missing {async_method}"


class TestV2GamesAPI:
    """Tests for V2 Games API."""

    def test_list_builds_correct_path(self):
        """list() should build correct nested path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"data": []}
        api = V2GamesAPI(mock_http)

        api.list("E", "2024")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v2/competitions/E/seasons/2024/games"

    def test_get_builds_correct_path(self):
        """get() should include game code in path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"game": {}}
        api = V2GamesAPI(mock_http)

        api.get("E", "2024", 1)

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v2/competitions/E/seasons/2024/games/1"

    def test_get_history_builds_correct_path(self):
        """get_history() should include history in path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"history": []}
        api = V2GamesAPI(mock_http)

        api.get_history("E", "2024", 1)

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v2/competitions/E/seasons/2024/games/1/history"


class TestSeasonsAPI:
    """Tests for V2 Seasons API."""

    def test_list_builds_correct_path(self):
        """list() should build correct path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"data": []}
        api = SeasonsAPI(mock_http)

        api.list("E")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v2/competitions/E/seasons"


class TestPlayerStatsAPI:
    """Tests for V3 Player Stats API."""

    def test_leaders_builds_correct_path(self):
        """leaders() should build correct path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"points": []}
        api = PlayerStatsAPI(mock_http)

        api.leaders("E")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v3/competitions/E/statistics/players/leaders"

    def test_leaders_with_params(self):
        """leaders() should pass params correctly."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"points": []}
        api = PlayerStatsAPI(mock_http)

        api.leaders(
            "E",
            season_mode="Single",
            season_code="E2024",
            team_code="BAR",
            limit=5,
        )

        call_args = mock_http.get.call_args
        params = call_args[1]["params"]
        assert params["SeasonMode"] == "Single"
        assert params["SeasonCode"] == "E2024"
        assert params["teamCode"] == "BAR"
        assert params["limit"] == 5

    def test_traditional_builds_correct_path(self):
        """traditional() should build correct path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"players": []}
        api = PlayerStatsAPI(mock_http)

        api.traditional("E")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v3/competitions/E/statistics/players/traditional"

    def test_advanced_builds_correct_path(self):
        """advanced() should build correct path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"players": []}
        api = PlayerStatsAPI(mock_http)

        api.advanced("E")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v3/competitions/E/statistics/players/advanced"


class TestTeamStatsAPI:
    """Tests for V3 Team Stats API."""

    def test_traditional_builds_correct_path(self):
        """traditional() should build correct path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"teams": []}
        api = TeamStatsAPI(mock_http)

        api.traditional("E")

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v3/competitions/E/statistics/teams/traditional"


class TestStandingsAPI:
    """Tests for V3 Standings API."""

    def test_basic_builds_correct_path(self):
        """basic() should build correct path."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"standings": []}
        api = StandingsAPI(mock_http)

        api.basic("E", "2024", 10)

        call_args = mock_http.get.call_args
        assert call_args[0][0] == "v3/competitions/E/seasons/2024/rounds/10/basicstandings"


class TestAsyncMethods:
    """Tests for async API methods."""

    @pytest.mark.asyncio
    async def test_async_method_calls_correct_path(self):
        """Async method should call correct path."""
        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value={"data": "test"})

        api = ClubsAPI(mock_http)
        result = await api.get_async("BAR")

        assert result == {"data": "test"}
        mock_http.get.assert_called_once()
        call_path = mock_http.get.call_args[0][0]
        assert call_path == "v2/clubs/BAR"

    @pytest.mark.asyncio
    async def test_async_method_with_params(self):
        """Async method should pass params correctly."""
        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value={"data": []})

        api = ClubsAPI(mock_http)
        await api.list_async(limit=5, offset=10)

        call_args = mock_http.get.call_args
        params = call_args[1]["params"]
        assert params["Limit"] == 5
        assert params["Offset"] == 10

    def test_async_methods_have_docstrings(self):
        """Async methods should have docstrings."""
        assert ClubsAPI.get_async.__doc__ is not None
        assert ClubsAPI.list_async.__doc__ is not None
