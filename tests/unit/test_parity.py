"""Tests for sync/async method parity across all API classes."""

import inspect

import pytest

# Import all API classes
from euroleague.api.v1.games import GamesAPI as V1GamesAPI
from euroleague.api.v1.players import PlayersAPI as V1PlayersAPI
from euroleague.api.v1.results import ResultsAPI as V1ResultsAPI
from euroleague.api.v1.schedules import SchedulesAPI as V1SchedulesAPI
from euroleague.api.v1.standings import StandingsAPI as V1StandingsAPI
from euroleague.api.v1.teams import TeamsAPI as V1TeamsAPI
from euroleague.api.v2.clubs import ClubsAPI
from euroleague.api.v2.competitions import CompetitionsAPI
from euroleague.api.v2.games import GamesAPI as V2GamesAPI
from euroleague.api.v2.groups import GroupsAPI
from euroleague.api.v2.people import PeopleAPI
from euroleague.api.v2.phases import PhasesAPI
from euroleague.api.v2.records import RecordsAPI
from euroleague.api.v2.referees import RefereesAPI
from euroleague.api.v2.rounds import RoundsAPI
from euroleague.api.v2.season_clubs import SeasonClubsAPI
from euroleague.api.v2.season_people import SeasonPeopleAPI
from euroleague.api.v2.seasons import SeasonsAPI
from euroleague.api.v2.standings import StandingsAPI as V2StandingsAPI
from euroleague.api.v2.stats import StatsAPI as V2StatsAPI
from euroleague.api.v3.clubs import ClubsAPI as V3ClubsAPI
from euroleague.api.v3.coaches import CoachesAPI
from euroleague.api.v3.games import GamesAPI as V3GamesAPI
from euroleague.api.v3.player_stats import PlayerStatsAPI
from euroleague.api.v3.standings import StandingsAPI as V3StandingsAPI
from euroleague.api.v3.stats import StatsAPI as V3StatsAPI
from euroleague.api.v3.team_stats import TeamStatsAPI

# All API classes to test
ALL_API_CLASSES = [
    # V1
    V1GamesAPI,
    V1PlayersAPI,
    V1ResultsAPI,
    V1SchedulesAPI,
    V1StandingsAPI,
    V1TeamsAPI,
    # V2
    ClubsAPI,
    CompetitionsAPI,
    V2GamesAPI,
    GroupsAPI,
    PeopleAPI,
    PhasesAPI,
    RecordsAPI,
    RefereesAPI,
    RoundsAPI,
    SeasonClubsAPI,
    SeasonPeopleAPI,
    SeasonsAPI,
    V2StandingsAPI,
    V2StatsAPI,
    # V3
    V3ClubsAPI,
    CoachesAPI,
    V3GamesAPI,
    PlayerStatsAPI,
    V3StandingsAPI,
    V3StatsAPI,
    TeamStatsAPI,
]


def get_public_methods(cls: type) -> list[str]:
    """Get all public methods (not starting with _) from a class."""
    methods = []
    for name in dir(cls):
        if name.startswith("_"):
            continue
        attr = getattr(cls, name, None)
        if callable(attr) and not isinstance(attr, type):
            methods.append(name)
    return methods


def get_method_signature(cls: type, method_name: str) -> inspect.Signature | None:
    """Get the signature of a method."""
    method = getattr(cls, method_name, None)
    if method is None:
        return None
    try:
        return inspect.signature(method)
    except ValueError:
        return None


class TestSyncAsyncParity:
    """Test that all sync methods have corresponding async methods."""

    @pytest.mark.parametrize("api_class", ALL_API_CLASSES)
    def test_all_sync_methods_have_async(self, api_class: type) -> None:
        """Every sync method should have a corresponding _async method."""
        methods = get_public_methods(api_class)

        sync_methods = [m for m in methods if not m.endswith("_async")]
        async_methods = set(m for m in methods if m.endswith("_async"))

        missing_async = []
        for sync_method in sync_methods:
            expected_async = f"{sync_method}_async"
            if expected_async not in async_methods:
                missing_async.append(sync_method)

        assert not missing_async, (
            f"{api_class.__name__} is missing async versions for: {missing_async}"
        )

    @pytest.mark.parametrize("api_class", ALL_API_CLASSES)
    def test_async_methods_have_matching_signatures(self, api_class: type) -> None:
        """Async methods should have same parameters as sync methods."""
        methods = get_public_methods(api_class)

        sync_methods = [m for m in methods if not m.endswith("_async")]

        for sync_method in sync_methods:
            async_method = f"{sync_method}_async"
            if not hasattr(api_class, async_method):
                continue  # Already caught by previous test

            sync_sig = get_method_signature(api_class, sync_method)
            async_sig = get_method_signature(api_class, async_method)

            if sync_sig is None or async_sig is None:
                continue

            # Compare parameters (excluding self)
            sync_params = list(sync_sig.parameters.keys())
            async_params = list(async_sig.parameters.keys())

            # Remove 'self' from comparison
            if sync_params and sync_params[0] == "self":
                sync_params = sync_params[1:]
            if async_params and async_params[0] == "self":
                async_params = async_params[1:]

            assert sync_params == async_params, (
                f"{api_class.__name__}.{sync_method} has params {sync_params} "
                f"but {async_method} has params {async_params}"
            )


class TestMethodCounts:
    """Test that we have the expected number of methods."""

    def test_total_api_classes(self) -> None:
        """Should have 27 API classes."""
        assert len(ALL_API_CLASSES) == 27

    def test_v1_has_6_classes(self) -> None:
        """V1 should have 6 API classes."""
        v1_count = sum(1 for c in ALL_API_CLASSES if "euroleague.api.v1" in c.__module__)
        assert v1_count == 6

    def test_v2_has_14_classes(self) -> None:
        """V2 should have 14 API classes."""
        v2_count = sum(1 for c in ALL_API_CLASSES if "euroleague.api.v2" in c.__module__)
        assert v2_count == 14

    def test_v3_has_7_classes(self) -> None:
        """V3 should have 7 API classes."""
        v3_count = sum(1 for c in ALL_API_CLASSES if "euroleague.api.v3" in c.__module__)
        assert v3_count == 7


class TestAsyncMethodProperties:
    """Test async method properties."""

    def test_async_methods_exist_at_class_level(self) -> None:
        """Async methods should exist at class definition time."""
        assert hasattr(ClubsAPI, "get_async")
        assert hasattr(ClubsAPI, "list_async")
        assert hasattr(PlayerStatsAPI, "leaders_async")

    def test_async_methods_are_coroutine_functions(self) -> None:
        """Async methods should be coroutine functions."""
        assert inspect.iscoroutinefunction(ClubsAPI.get_async)
        assert inspect.iscoroutinefunction(ClubsAPI.list_async)
        assert inspect.iscoroutinefunction(PlayerStatsAPI.leaders_async)

    def test_sync_methods_are_not_coroutine_functions(self) -> None:
        """Sync methods should not be coroutine functions."""
        assert not inspect.iscoroutinefunction(ClubsAPI.get)
        assert not inspect.iscoroutinefunction(ClubsAPI.list)
        assert not inspect.iscoroutinefunction(PlayerStatsAPI.leaders)

    def test_async_methods_have_docstrings(self) -> None:
        """Async methods should have docstrings."""
        assert ClubsAPI.get_async.__doc__ is not None
        assert ClubsAPI.list_async.__doc__ is not None

    def test_referees_async_methods_exist(self) -> None:
        """RefereesAPI should have all async methods."""
        assert hasattr(RefereesAPI, "list_async")
        assert hasattr(RefereesAPI, "get_async")
        assert hasattr(RefereesAPI, "list_by_competition_async")
        assert hasattr(RefereesAPI, "list_by_season_async")
