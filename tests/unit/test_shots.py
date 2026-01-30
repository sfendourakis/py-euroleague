"""Unit tests for Shots API and models."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from euroleague.api.live.shots import ShotsAPI
from euroleague.models.live.shots import Shot, ShotsResponse


class TestShotsAPI:
    """Tests for ShotsAPI class."""

    def test_get_builds_correct_path(self):
        """get() should build correct path with Points endpoint."""
        mock_http = MagicMock()
        mock_http.get.return_value = {"Rows": []}
        api = ShotsAPI(mock_http)

        api.get(season_code="E2025", game_code=241)

        mock_http.get.assert_called_once()
        call_args = mock_http.get.call_args
        assert call_args[0][0] == "Points"
        assert call_args[1]["params"] == {"seasoncode": "E2025", "gamecode": 241}

    def test_get_returns_parsed_model(self):
        """get() should return ShotsResponse model."""
        mock_http = MagicMock()
        mock_http.get.return_value = {
            "Rows": [
                {
                    "NUM_ANOT": 1,
                    "TEAM": "MAD       ",
                    "ID_PLAYER": "P001",
                    "PLAYER": "DOE, JOHN",
                    "ID_ACTION": "2FGM",
                    "ACTION": "Two Pointer",
                    "POINTS": 2,
                    "COORD_X": 150,
                    "COORD_Y": 280,
                    "ZONE": "C",
                    "FASTBREAK": 0,
                    "SECOND_CHANCE": 0,
                    "POINTS_OFF_TURNOVER": 0,
                    "MINUTE": 5,
                    "CONSOLE": "04:32",
                    "POINTS_A": 10,
                    "POINTS_B": 8,
                    "UTC": "20250115193245",
                }
            ]
        }
        api = ShotsAPI(mock_http)

        result = api.get("E2025", 241)

        assert isinstance(result, ShotsResponse)
        assert len(result.rows) == 1
        assert result.rows[0].player == "DOE, JOHN"
        assert result.rows[0].coord_x == 150
        assert result.rows[0].coord_y == 280

    def test_get_raw_returns_dict(self):
        """get_raw() should return raw dictionary without parsing."""
        mock_http = MagicMock()
        raw_data = {
            "Rows": [],
            "ExtraField": "should be preserved",
        }
        mock_http.get.return_value = raw_data
        api = ShotsAPI(mock_http)

        result = api.get_raw("E2025", 241)

        assert isinstance(result, dict)
        assert result["ExtraField"] == "should be preserved"

    @pytest.mark.asyncio
    async def test_get_async_works(self):
        """get_async() should work correctly."""
        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value={"Rows": []})
        api = ShotsAPI(mock_http)

        result = await api.get_async("E2025", 241)

        assert isinstance(result, ShotsResponse)
        mock_http.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_raw_async_works(self):
        """get_raw_async() should work correctly."""
        mock_http = MagicMock()
        mock_http.get = AsyncMock(return_value={"Rows": []})
        api = ShotsAPI(mock_http)

        result = await api.get_raw_async("E2025", 241)

        assert isinstance(result, dict)


class TestShot:
    """Tests for Shot model."""

    def test_shot_parses_correctly(self):
        """Shot should parse API response correctly."""
        data = {
            "NUM_ANOT": 5,
            "TEAM": "BAR       ",
            "ID_PLAYER": "P123",
            "PLAYER": "SMITH, JANE",
            "ID_ACTION": "3FGM",
            "ACTION": "Three Pointer",
            "POINTS": 3,
            "COORD_X": 200,
            "COORD_Y": 100,
            "ZONE": "E",
            "FASTBREAK": 1,
            "SECOND_CHANCE": 0,
            "POINTS_OFF_TURNOVER": 1,
            "MINUTE": 7,
            "CONSOLE": "02:15",
            "POINTS_A": 25,
            "POINTS_B": 22,
            "UTC": "20250115194530",
        }

        shot = Shot.model_validate(data)

        assert shot.num_anot == 5
        assert shot.team == "BAR"  # Whitespace is stripped by base model
        assert shot.team_code == "BAR"
        assert shot.player_id == "P123"
        assert shot.player == "SMITH, JANE"
        assert shot.action_id == "3FGM"
        assert shot.action == "Three Pointer"
        assert shot.points == 3
        assert shot.coord_x == 200
        assert shot.coord_y == 100
        assert shot.zone == "E"
        assert shot.fastbreak is True
        assert shot.second_chance is False
        assert shot.points_off_turnover is True
        assert shot.minute == 7
        assert shot.console == "02:15"
        assert shot.points_a == 25
        assert shot.points_b == 22

    def test_is_made_for_made_shots(self):
        """is_made should return True for made shots."""
        base_data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ACTION": "Test",
            "POINTS": 0,
            "COORD_X": 100,
            "COORD_Y": 100,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        for action_id in ["2FGM", "3FGM", "FTM"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_made is True, f"{action_id} should be made"

    def test_is_made_for_missed_shots(self):
        """is_made should return False for missed shots."""
        base_data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ACTION": "Test",
            "POINTS": 0,
            "COORD_X": 100,
            "COORD_Y": 100,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        for action_id in ["2FGA", "3FGA", "FTA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_made is False, f"{action_id} should be missed"

    def test_is_missed(self):
        """is_missed should correctly identify missed shots."""
        base_data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ACTION": "Test",
            "POINTS": 0,
            "COORD_X": 100,
            "COORD_Y": 100,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        for action_id in ["2FGA", "3FGA", "FTA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_missed is True, f"{action_id} should be missed"

        for action_id in ["2FGM", "3FGM", "FTM"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_missed is False, f"{action_id} should not be missed"

    def test_is_three_pointer(self):
        """is_three_pointer should identify 3-point attempts."""
        base_data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ACTION": "Test",
            "POINTS": 0,
            "COORD_X": 100,
            "COORD_Y": 100,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        for action_id in ["3FGM", "3FGA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_three_pointer is True

        for action_id in ["2FGM", "2FGA", "FTM", "FTA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_three_pointer is False

    def test_is_two_pointer(self):
        """is_two_pointer should identify 2-point attempts."""
        base_data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ACTION": "Test",
            "POINTS": 0,
            "COORD_X": 100,
            "COORD_Y": 100,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        for action_id in ["2FGM", "2FGA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_two_pointer is True

        for action_id in ["3FGM", "3FGA", "FTM", "FTA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_two_pointer is False

    def test_is_free_throw(self):
        """is_free_throw should identify free throw attempts."""
        base_data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ACTION": "Test",
            "POINTS": 0,
            "COORD_X": -1,
            "COORD_Y": -1,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        for action_id in ["FTM", "FTA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_free_throw is True

        for action_id in ["2FGM", "2FGA", "3FGM", "3FGA"]:
            data = {**base_data, "ID_ACTION": action_id}
            shot = Shot.model_validate(data)
            assert shot.is_free_throw is False

    def test_has_coordinates(self):
        """has_coordinates should check for valid coordinates."""
        base_data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ID_ACTION": "2FGM",
            "ACTION": "Test",
            "POINTS": 2,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        # Valid coordinates
        data = {**base_data, "COORD_X": 150, "COORD_Y": 200}
        shot = Shot.model_validate(data)
        assert shot.has_coordinates is True

        # Free throw coordinates (invalid)
        data = {**base_data, "COORD_X": -1, "COORD_Y": -1}
        shot = Shot.model_validate(data)
        assert shot.has_coordinates is False

        # Zero coordinates (valid - corner of court)
        data = {**base_data, "COORD_X": 0, "COORD_Y": 0}
        shot = Shot.model_validate(data)
        assert shot.has_coordinates is True

    def test_team_code_strips_whitespace(self):
        """team_code should strip whitespace from team field."""
        data = {
            "NUM_ANOT": 1,
            "TEAM": "MAD       ",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ID_ACTION": "2FGM",
            "ACTION": "Test",
            "POINTS": 2,
            "COORD_X": 100,
            "COORD_Y": 100,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        shot = Shot.model_validate(data)
        assert shot.team_code == "MAD"

    def test_boolean_field_conversion(self):
        """Boolean fields should convert from int (0/1)."""
        data = {
            "NUM_ANOT": 1,
            "TEAM": "A",
            "ID_PLAYER": "P1",
            "PLAYER": "Test",
            "ID_ACTION": "2FGM",
            "ACTION": "Test",
            "POINTS": 2,
            "COORD_X": 100,
            "COORD_Y": 100,
            "FASTBREAK": 1,
            "SECOND_CHANCE": 0,
            "POINTS_OFF_TURNOVER": 1,
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

        shot = Shot.model_validate(data)
        assert shot.fastbreak is True
        assert shot.second_chance is False
        assert shot.points_off_turnover is True


class TestShotsResponse:
    """Tests for ShotsResponse model."""

    def _create_shot_data(
        self, action_id: str, team: str = "A", player_id: str = "P1", zone: str = "C"
    ):
        """Helper to create shot data."""
        return {
            "NUM_ANOT": 1,
            "TEAM": team,
            "ID_PLAYER": player_id,
            "PLAYER": "Test",
            "ID_ACTION": action_id,
            "ACTION": "Test",
            "POINTS": 2 if "2" in action_id else (3 if "3" in action_id else 1),
            "COORD_X": 100 if not action_id.startswith("FT") else -1,
            "COORD_Y": 100 if not action_id.startswith("FT") else -1,
            "ZONE": zone if not action_id.startswith("FT") else "",
            "MINUTE": 1,
            "CONSOLE": "10:00",
            "POINTS_A": 0,
            "POINTS_B": 0,
        }

    def test_all_shots_returns_rows(self):
        """all_shots should return all rows."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("3FGA"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        assert len(response.all_shots) == 2

    def test_total_shots_returns_count(self):
        """total_shots should return count of all shots."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("3FGA"),
                self._create_shot_data("FTM"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        assert response.total_shots == 3

    def test_made_shots_filters_correctly(self):
        """made_shots should return only made shots."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("2FGA"),
                self._create_shot_data("3FGM"),
                self._create_shot_data("3FGA"),
                self._create_shot_data("FTM"),
                self._create_shot_data("FTA"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        made = response.made_shots
        assert len(made) == 3
        assert all(s.is_made for s in made)

    def test_missed_shots_filters_correctly(self):
        """missed_shots should return only missed shots."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("2FGA"),
                self._create_shot_data("3FGA"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        missed = response.missed_shots
        assert len(missed) == 2
        assert all(s.is_missed for s in missed)

    def test_field_goals_excludes_free_throws(self):
        """field_goals should exclude free throws."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("3FGA"),
                self._create_shot_data("FTM"),
                self._create_shot_data("FTA"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        fg = response.field_goals
        assert len(fg) == 2
        assert all(not s.is_free_throw for s in fg)

    def test_three_pointers_filters_correctly(self):
        """three_pointers should return only 3-point attempts."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("3FGM"),
                self._create_shot_data("3FGA"),
                self._create_shot_data("FTM"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        threes = response.three_pointers
        assert len(threes) == 2
        assert all(s.is_three_pointer for s in threes)

    def test_two_pointers_filters_correctly(self):
        """two_pointers should return only 2-point attempts."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("2FGA"),
                self._create_shot_data("3FGM"),
                self._create_shot_data("FTM"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        twos = response.two_pointers
        assert len(twos) == 2
        assert all(s.is_two_pointer for s in twos)

    def test_free_throws_filters_correctly(self):
        """free_throws should return only free throw attempts."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("FTM"),
                self._create_shot_data("FTA"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        ft = response.free_throws
        assert len(ft) == 2
        assert all(s.is_free_throw for s in ft)

    def test_get_shots_by_team(self):
        """get_shots_by_team should filter by team code."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM", team="MAD       "),
                self._create_shot_data("3FGM", team="BAR       "),
                self._create_shot_data("2FGA", team="MAD       "),
            ]
        }
        response = ShotsResponse.model_validate(data)
        mad_shots = response.get_shots_by_team("MAD")
        bar_shots = response.get_shots_by_team("BAR")
        assert len(mad_shots) == 2
        assert len(bar_shots) == 1

    def test_get_shots_by_player(self):
        """get_shots_by_player should filter by player ID."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM", player_id="P001"),
                self._create_shot_data("3FGM", player_id="P002"),
                self._create_shot_data("2FGA", player_id="P001"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        player_shots = response.get_shots_by_player("P001")
        assert len(player_shots) == 2

    def test_get_shots_by_zone(self):
        """get_shots_by_zone should filter by court zone."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM", zone="A"),
                self._create_shot_data("3FGM", zone="E"),
                self._create_shot_data("2FGA", zone="A"),
                self._create_shot_data("2FGM", zone="C"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        zone_a = response.get_shots_by_zone("A")
        zone_e = response.get_shots_by_zone("E")
        assert len(zone_a) == 2
        assert len(zone_e) == 1

    def test_get_shooting_percentage(self):
        """get_shooting_percentage should calculate correct percentage."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("2FGA"),
                self._create_shot_data("2FGM"),
                self._create_shot_data("2FGA"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        pct = response.get_shooting_percentage()
        assert pct == 50.0

    def test_get_shooting_percentage_empty(self):
        """get_shooting_percentage should return 0.0 for empty list."""
        data = {"Rows": []}
        response = ShotsResponse.model_validate(data)
        assert response.get_shooting_percentage() == 0.0

    def test_get_shooting_percentage_with_shots_arg(self):
        """get_shooting_percentage should accept custom shot list."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("2FGA"),
                self._create_shot_data("3FGM"),
                self._create_shot_data("3FGA"),
                self._create_shot_data("3FGA"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        threes_pct = response.get_shooting_percentage(response.three_pointers)
        assert threes_pct == pytest.approx(33.33, rel=0.01)

    def test_get_field_goal_percentage(self):
        """get_field_goal_percentage should exclude free throws."""
        data = {
            "Rows": [
                self._create_shot_data("2FGM"),
                self._create_shot_data("2FGA"),
                self._create_shot_data("FTM"),
                self._create_shot_data("FTM"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        fg_pct = response.get_field_goal_percentage()
        assert fg_pct == 50.0

    def test_get_three_point_percentage(self):
        """get_three_point_percentage should calculate 3PT%."""
        data = {
            "Rows": [
                self._create_shot_data("3FGM"),
                self._create_shot_data("3FGA"),
                self._create_shot_data("3FGA"),
                self._create_shot_data("2FGM"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        three_pct = response.get_three_point_percentage()
        assert three_pct == pytest.approx(33.33, rel=0.01)

    def test_get_free_throw_percentage(self):
        """get_free_throw_percentage should calculate FT%."""
        data = {
            "Rows": [
                self._create_shot_data("FTM"),
                self._create_shot_data("FTM"),
                self._create_shot_data("FTA"),
                self._create_shot_data("2FGM"),
            ]
        }
        response = ShotsResponse.model_validate(data)
        ft_pct = response.get_free_throw_percentage()
        assert ft_pct == pytest.approx(66.67, rel=0.01)


class TestClientIntegration:
    """Tests for client integration with ShotsAPI."""

    def test_client_has_shots_api(self):
        """EuroleagueClient should have shots API on live."""
        from euroleague import EuroleagueClient

        client = EuroleagueClient()
        assert hasattr(client, "live")
        assert hasattr(client.live, "shots")
        client.close()

    def test_async_client_has_shots_api(self):
        """AsyncEuroleagueClient should have shots API on live."""
        from euroleague import AsyncEuroleagueClient

        client = AsyncEuroleagueClient()
        assert hasattr(client, "live")
        assert hasattr(client.live, "shots")
