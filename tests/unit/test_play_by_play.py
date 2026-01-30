"""Unit tests for Play-by-Play API and models."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from euroleague.api.live.play_by_play import PlayByPlayAPI
from euroleague.models.live.play_by_play import PlayByPlayResponse, PlayEvent


class TestPlayByPlayAPI:
    """Tests for PlayByPlayAPI class."""

    def test_get_builds_correct_path(self):
        """get() should build correct path with PlayByPlay endpoint."""
        mock_http = MagicMock()
        mock_http.get.return_value = {
            "Live": False,
            "TeamA": "Test A",
            "TeamB": "Test B",
            "CodeTeamA": "TSA",
            "CodeTeamB": "TSB",
            "ActualQuarter": 4,
            "FirstQuarter": [],
            "SecondQuarter": [],
            "ThirdQuarter": [],
            "FourthQuarter": [],
        }
        api = PlayByPlayAPI(mock_http)

        api.get(season_code="E2025", game_code=241)

        mock_http.get.assert_called_once()
        call_args = mock_http.get.call_args
        assert call_args[0][0] == "PlayByPlay"
        assert call_args[1]["params"] == {"seasoncode": "E2025", "gamecode": 241}

    def test_get_returns_parsed_model(self):
        """get() should return PlayByPlayResponse model."""
        mock_http = MagicMock()
        mock_http.get.return_value = {
            "Live": False,
            "TeamA": "Real Madrid",
            "TeamB": "Barcelona",
            "CodeTeamA": "MAD",
            "CodeTeamB": "BAR",
            "ActualQuarter": 4,
            "FirstQuarter": [
                {
                    "NUMBEROFPLAY": 1,
                    "PLAYTYPE": "2FGM",
                    "PLAYER": "Player A",
                    "PLAYER_ID": "P001",
                    "TEAM": "Real Madrid",
                    "CODETEAM": "MAD",
                    "DORSAL": "7",
                    "MINUTE": 1,
                    "MARKERTIME": "09:45",
                    "POINTS_A": 2,
                    "POINTS_B": 0,
                    "PLAYINFO": "Two Pointer",
                    "COMMENT": "",
                    "TYPE": 0,
                }
            ],
            "SecondQuarter": [],
            "ThirdQuarter": [],
            "FourthQuarter": [],
        }
        api = PlayByPlayAPI(mock_http)

        result = api.get("E2025", 241)

        assert isinstance(result, PlayByPlayResponse)
        assert result.team_a == "Real Madrid"
        assert result.team_b == "Barcelona"
        assert len(result.first_quarter) == 1
        assert result.first_quarter[0].player == "Player A"

    def test_get_raw_returns_dict(self):
        """get_raw() should return raw dictionary without parsing."""
        mock_http = MagicMock()
        raw_data = {
            "Live": False,
            "TeamA": "Test",
            "TeamB": "Test2",
            "CodeTeamA": "TST",
            "CodeTeamB": "TS2",
            "ActualQuarter": 4,
            "FirstQuarter": [],
            "SecondQuarter": [],
            "ThirdQuarter": [],
            "FourthQuarter": [],
            "ExtraField": "should be preserved",
        }
        mock_http.get.return_value = raw_data
        api = PlayByPlayAPI(mock_http)

        result = api.get_raw("E2025", 241)

        assert isinstance(result, dict)
        assert result["ExtraField"] == "should be preserved"

    @pytest.mark.asyncio
    async def test_get_async_works(self):
        """get_async() should work correctly."""
        mock_http = MagicMock()
        mock_http.get = AsyncMock(
            return_value={
                "Live": False,
                "TeamA": "Test",
                "TeamB": "Test2",
                "CodeTeamA": "TST",
                "CodeTeamB": "TS2",
                "ActualQuarter": 4,
                "FirstQuarter": [],
                "SecondQuarter": [],
                "ThirdQuarter": [],
                "FourthQuarter": [],
            }
        )
        api = PlayByPlayAPI(mock_http)

        result = await api.get_async("E2025", 241)

        assert isinstance(result, PlayByPlayResponse)
        mock_http.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_raw_async_works(self):
        """get_raw_async() should work correctly."""
        mock_http = MagicMock()
        mock_http.get = AsyncMock(
            return_value={
                "Live": False,
                "TeamA": "Test",
                "TeamB": "Test2",
                "CodeTeamA": "TST",
                "CodeTeamB": "TS2",
                "ActualQuarter": 4,
                "FirstQuarter": [],
                "SecondQuarter": [],
                "ThirdQuarter": [],
                "FourthQuarter": [],
            }
        )
        api = PlayByPlayAPI(mock_http)

        result = await api.get_raw_async("E2025", 241)

        assert isinstance(result, dict)


class TestPlayEvent:
    """Tests for PlayEvent model."""

    def test_play_event_parses_correctly(self):
        """PlayEvent should parse API response correctly."""
        data = {
            "NUMBEROFPLAY": 5,
            "PLAYTYPE": "3FGM",
            "PLAYER": "John Doe",
            "PLAYER_ID": "P123",
            "TEAM": "Team A",
            "CODETEAM": "TMA",
            "DORSAL": "23",
            "MINUTE": 3,
            "MARKERTIME": "07:30",
            "POINTS_A": 15,
            "POINTS_B": 12,
            "PLAYINFO": "Three Pointer Made",
            "COMMENT": "Good shot",
            "TYPE": 0,
        }

        event = PlayEvent.model_validate(data)

        assert event.number_of_play == 5
        assert event.play_type == "3FGM"
        assert event.player == "John Doe"
        assert event.player_id == "P123"
        assert event.team == "Team A"
        assert event.team_code == "TMA"
        assert event.dorsal == "23"
        assert event.minute == 3
        assert event.marker_time == "07:30"
        assert event.points_a == 15
        assert event.points_b == 12
        assert event.play_info == "Three Pointer Made"

    def test_is_scoring_play_for_made_shots(self):
        """is_scoring_play should return True for made shots."""
        data_3pt = {
            "PLAYTYPE": "3FGM",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }
        data_2pt = {
            "PLAYTYPE": "2FGM",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }
        data_ft = {
            "PLAYTYPE": "FTM",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }

        assert PlayEvent.model_validate(data_3pt).is_scoring_play is True
        assert PlayEvent.model_validate(data_2pt).is_scoring_play is True
        assert PlayEvent.model_validate(data_ft).is_scoring_play is True

    def test_is_scoring_play_for_missed_shots(self):
        """is_scoring_play should return False for missed shots."""
        data_3pt = {
            "PLAYTYPE": "3FGA",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }
        data_2pt = {
            "PLAYTYPE": "2FGA",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }

        assert PlayEvent.model_validate(data_3pt).is_scoring_play is False
        assert PlayEvent.model_validate(data_2pt).is_scoring_play is False

    def test_points_scored_returns_correct_values(self):
        """points_scored should return correct point values."""
        data_3pt = {
            "PLAYTYPE": "3FGM",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }
        data_2pt = {
            "PLAYTYPE": "2FGM",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }
        data_ft = {
            "PLAYTYPE": "FTM",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }
        data_miss = {
            "PLAYTYPE": "3FGA",
            "NUMBEROFPLAY": 1,
            "PLAYER_ID": "P1",
            "CODETEAM": "A",
            "DORSAL": "1",
            "MINUTE": 1,
            "MARKERTIME": "10:00",
        }

        assert PlayEvent.model_validate(data_3pt).points_scored == 3
        assert PlayEvent.model_validate(data_2pt).points_scored == 2
        assert PlayEvent.model_validate(data_ft).points_scored == 1
        assert PlayEvent.model_validate(data_miss).points_scored == 0

    def test_is_shot_attempt(self):
        """is_shot_attempt should identify all shot types."""
        shot_types = ["2FGM", "2FGA", "3FGM", "3FGA", "FTM", "FTA"]
        non_shot_types = ["AS", "TO", "ST", "D", "O", "CM", "RV"]

        for play_type in shot_types:
            data = {
                "PLAYTYPE": play_type,
                "NUMBEROFPLAY": 1,
                "PLAYER_ID": "P1",
                "CODETEAM": "A",
                "DORSAL": "1",
                "MINUTE": 1,
                "MARKERTIME": "10:00",
            }
            assert PlayEvent.model_validate(data).is_shot_attempt is True, (
                f"{play_type} should be a shot attempt"
            )

        for play_type in non_shot_types:
            data = {
                "PLAYTYPE": play_type,
                "NUMBEROFPLAY": 1,
                "PLAYER_ID": "P1",
                "CODETEAM": "A",
                "DORSAL": "1",
                "MINUTE": 1,
                "MARKERTIME": "10:00",
            }
            assert PlayEvent.model_validate(data).is_shot_attempt is False, (
                f"{play_type} should not be a shot attempt"
            )


class TestPlayByPlayResponse:
    """Tests for PlayByPlayResponse model."""

    def test_all_plays_combines_quarters(self):
        """all_plays should combine all quarters in order."""
        data = {
            "Live": False,
            "TeamA": "A",
            "TeamB": "B",
            "CodeTeamA": "A",
            "CodeTeamB": "B",
            "ActualQuarter": 4,
            "FirstQuarter": [
                {
                    "PLAYTYPE": "2FGM",
                    "NUMBEROFPLAY": 1,
                    "PLAYER_ID": "P1",
                    "CODETEAM": "A",
                    "DORSAL": "1",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
            "SecondQuarter": [
                {
                    "PLAYTYPE": "3FGM",
                    "NUMBEROFPLAY": 2,
                    "PLAYER_ID": "P2",
                    "CODETEAM": "B",
                    "DORSAL": "2",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
            "ThirdQuarter": [
                {
                    "PLAYTYPE": "FTM",
                    "NUMBEROFPLAY": 3,
                    "PLAYER_ID": "P3",
                    "CODETEAM": "A",
                    "DORSAL": "3",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
            "FourthQuarter": [
                {
                    "PLAYTYPE": "AS",
                    "NUMBEROFPLAY": 4,
                    "PLAYER_ID": "P4",
                    "CODETEAM": "B",
                    "DORSAL": "4",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
        }

        response = PlayByPlayResponse.model_validate(data)
        all_plays = response.all_plays

        assert len(all_plays) == 4
        assert all_plays[0].play_type == "2FGM"
        assert all_plays[1].play_type == "3FGM"
        assert all_plays[2].play_type == "FTM"
        assert all_plays[3].play_type == "AS"

    def test_total_plays_returns_count(self):
        """total_plays should return correct count."""
        data = {
            "Live": False,
            "TeamA": "A",
            "TeamB": "B",
            "CodeTeamA": "A",
            "CodeTeamB": "B",
            "ActualQuarter": 4,
            "FirstQuarter": [
                {
                    "PLAYTYPE": "2FGM",
                    "NUMBEROFPLAY": 1,
                    "PLAYER_ID": "P1",
                    "CODETEAM": "A",
                    "DORSAL": "1",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
            "SecondQuarter": [
                {
                    "PLAYTYPE": "3FGM",
                    "NUMBEROFPLAY": 2,
                    "PLAYER_ID": "P2",
                    "CODETEAM": "B",
                    "DORSAL": "2",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                },
                {
                    "PLAYTYPE": "TO",
                    "NUMBEROFPLAY": 3,
                    "PLAYER_ID": "P3",
                    "CODETEAM": "A",
                    "DORSAL": "3",
                    "MINUTE": 2,
                    "MARKERTIME": "09:00",
                },
            ],
            "ThirdQuarter": [],
            "FourthQuarter": [],
        }

        response = PlayByPlayResponse.model_validate(data)

        assert response.total_plays == 3

    def test_get_quarter_returns_correct_quarter(self):
        """get_quarter() should return correct quarter plays."""
        data = {
            "Live": False,
            "TeamA": "A",
            "TeamB": "B",
            "CodeTeamA": "A",
            "CodeTeamB": "B",
            "ActualQuarter": 4,
            "FirstQuarter": [
                {
                    "PLAYTYPE": "Q1",
                    "NUMBEROFPLAY": 1,
                    "PLAYER_ID": "P1",
                    "CODETEAM": "A",
                    "DORSAL": "1",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
            "SecondQuarter": [
                {
                    "PLAYTYPE": "Q2",
                    "NUMBEROFPLAY": 2,
                    "PLAYER_ID": "P2",
                    "CODETEAM": "B",
                    "DORSAL": "2",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
            "ThirdQuarter": [
                {
                    "PLAYTYPE": "Q3",
                    "NUMBEROFPLAY": 3,
                    "PLAYER_ID": "P3",
                    "CODETEAM": "A",
                    "DORSAL": "3",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
            "FourthQuarter": [
                {
                    "PLAYTYPE": "Q4",
                    "NUMBEROFPLAY": 4,
                    "PLAYER_ID": "P4",
                    "CODETEAM": "B",
                    "DORSAL": "4",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                }
            ],
        }

        response = PlayByPlayResponse.model_validate(data)

        assert response.get_quarter(1)[0].play_type == "Q1"
        assert response.get_quarter(2)[0].play_type == "Q2"
        assert response.get_quarter(3)[0].play_type == "Q3"
        assert response.get_quarter(4)[0].play_type == "Q4"
        assert response.get_quarter(99) == []  # Invalid quarter

    def test_get_plays_by_team(self):
        """get_plays_by_team() should filter by team code."""
        data = {
            "Live": False,
            "TeamA": "A",
            "TeamB": "B",
            "CodeTeamA": "TMA",
            "CodeTeamB": "TMB",
            "ActualQuarter": 4,
            "FirstQuarter": [
                {
                    "PLAYTYPE": "2FGM",
                    "NUMBEROFPLAY": 1,
                    "PLAYER_ID": "P1",
                    "CODETEAM": "TMA",
                    "DORSAL": "1",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                },
                {
                    "PLAYTYPE": "3FGM",
                    "NUMBEROFPLAY": 2,
                    "PLAYER_ID": "P2",
                    "CODETEAM": "TMB",
                    "DORSAL": "2",
                    "MINUTE": 2,
                    "MARKERTIME": "09:00",
                },
                {
                    "PLAYTYPE": "FTM",
                    "NUMBEROFPLAY": 3,
                    "PLAYER_ID": "P3",
                    "CODETEAM": "TMA",
                    "DORSAL": "3",
                    "MINUTE": 3,
                    "MARKERTIME": "08:00",
                },
            ],
            "SecondQuarter": [],
            "ThirdQuarter": [],
            "FourthQuarter": [],
        }

        response = PlayByPlayResponse.model_validate(data)
        team_a_plays = response.get_plays_by_team("TMA")
        team_b_plays = response.get_plays_by_team("TMB")

        assert len(team_a_plays) == 2
        assert len(team_b_plays) == 1

    def test_get_plays_by_player(self):
        """get_plays_by_player() should filter by player ID."""
        data = {
            "Live": False,
            "TeamA": "A",
            "TeamB": "B",
            "CodeTeamA": "A",
            "CodeTeamB": "B",
            "ActualQuarter": 4,
            "FirstQuarter": [
                {
                    "PLAYTYPE": "2FGM",
                    "NUMBEROFPLAY": 1,
                    "PLAYER_ID": "P001",
                    "CODETEAM": "A",
                    "DORSAL": "1",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                },
                {
                    "PLAYTYPE": "3FGM",
                    "NUMBEROFPLAY": 2,
                    "PLAYER_ID": "P002",
                    "CODETEAM": "B",
                    "DORSAL": "2",
                    "MINUTE": 2,
                    "MARKERTIME": "09:00",
                },
                {
                    "PLAYTYPE": "AS",
                    "NUMBEROFPLAY": 3,
                    "PLAYER_ID": "P001",
                    "CODETEAM": "A",
                    "DORSAL": "1",
                    "MINUTE": 3,
                    "MARKERTIME": "08:00",
                },
            ],
            "SecondQuarter": [],
            "ThirdQuarter": [],
            "FourthQuarter": [],
        }

        response = PlayByPlayResponse.model_validate(data)
        player_plays = response.get_plays_by_player("P001")

        assert len(player_plays) == 2

    def test_get_scoring_plays(self):
        """get_scoring_plays() should return only scoring plays."""
        data = {
            "Live": False,
            "TeamA": "A",
            "TeamB": "B",
            "CodeTeamA": "A",
            "CodeTeamB": "B",
            "ActualQuarter": 4,
            "FirstQuarter": [
                {
                    "PLAYTYPE": "2FGM",
                    "NUMBEROFPLAY": 1,
                    "PLAYER_ID": "P1",
                    "CODETEAM": "A",
                    "DORSAL": "1",
                    "MINUTE": 1,
                    "MARKERTIME": "10:00",
                },
                {
                    "PLAYTYPE": "2FGA",
                    "NUMBEROFPLAY": 2,
                    "PLAYER_ID": "P2",
                    "CODETEAM": "B",
                    "DORSAL": "2",
                    "MINUTE": 2,
                    "MARKERTIME": "09:00",
                },
                {
                    "PLAYTYPE": "3FGM",
                    "NUMBEROFPLAY": 3,
                    "PLAYER_ID": "P3",
                    "CODETEAM": "A",
                    "DORSAL": "3",
                    "MINUTE": 3,
                    "MARKERTIME": "08:00",
                },
                {
                    "PLAYTYPE": "TO",
                    "NUMBEROFPLAY": 4,
                    "PLAYER_ID": "P4",
                    "CODETEAM": "B",
                    "DORSAL": "4",
                    "MINUTE": 4,
                    "MARKERTIME": "07:00",
                },
                {
                    "PLAYTYPE": "FTM",
                    "NUMBEROFPLAY": 5,
                    "PLAYER_ID": "P5",
                    "CODETEAM": "A",
                    "DORSAL": "5",
                    "MINUTE": 5,
                    "MARKERTIME": "06:00",
                },
            ],
            "SecondQuarter": [],
            "ThirdQuarter": [],
            "FourthQuarter": [],
        }

        response = PlayByPlayResponse.model_validate(data)
        scoring_plays = response.get_scoring_plays()

        assert len(scoring_plays) == 3
        assert all(p.is_scoring_play for p in scoring_plays)


class TestClientIntegration:
    """Tests for client integration with LiveAPI."""

    def test_client_has_live_property(self):
        """EuroleagueClient should have live property."""
        from euroleague import EuroleagueClient

        client = EuroleagueClient()
        assert hasattr(client, "live")
        assert hasattr(client.live, "play_by_play")
        client.close()

    def test_async_client_has_live_property(self):
        """AsyncEuroleagueClient should have live property."""
        from euroleague import AsyncEuroleagueClient

        client = AsyncEuroleagueClient()
        assert hasattr(client, "live")
        assert hasattr(client.live, "play_by_play")
