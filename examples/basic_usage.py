"""Basic usage example for py-euroleague."""

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError, NotFoundError

# Initialize the client
client = EuroleagueClient()


def example_v2_api():
    """V2 API examples (comprehensive endpoints)."""
    print("\n--- V2 API Examples ---")

    # List clubs (default limit is 20, but there are 400+ total)
    clubs = client.v2.clubs.list(limit=50)
    total_clubs = clubs.get("total", 0)
    print(f"V2 Clubs: Fetched {len(clubs.get('data', []))}, Total available: {total_clubs}")

    # Get specific club
    try:
        barcelona = client.v2.clubs.get("BAR")
        print(f"V2 Barcelona: {barcelona.get('name', 'N/A')}")
    except NotFoundError:
        print("V2 Barcelona: Not found")

    # List competitions
    competitions = client.v2.competitions.list()
    print(f"V2 Competitions: Found {len(competitions.get('data', []))} competitions")

    # List seasons for Euroleague
    seasons = client.v2.seasons.list(competition_code="E", limit=5)
    print(f"V2 Recent seasons: {[s.get('code') for s in seasons.get('data', [])]}")


def example_v3_api():
    """V3 API examples (statistics-focused endpoints)."""
    print("\n--- V3 API Examples ---")

    # Get player leaders for current season (E2025)
    try:
        leaders = client.v3.player_stats.leaders(
            competition_code="E", season_mode="Single", season_code="E2025", limit=3
        )
        # Leaders returns categories like 'points', 'rebounds', etc.
        points_leaders = leaders.get("points", [])
        print("V3 Points Leaders (E2025):")
        for player in points_leaders[:3]:
            details = player.get("details", {})
            print(
                f"  {player.get('rank')}. {details.get('name')} - {player.get('average'):.1f} ppg"
            )
    except APIError as e:
        print(f"V3 Player Leaders: API error - {e}")

    # Get team stats (note: response uses 'teams' key, not 'data')
    try:
        team_stats = client.v3.team_stats.traditional(
            competition_code="E",
            season_mode="Single",
            season_code="E2025",
        )
        teams = team_stats.get("teams", [])
        print(f"V3 Team Stats (E2025): Found {len(teams)} teams")
        for team in teams[:3]:
            team_info = team.get("team", {})
            print(f"  - {team_info.get('name')}: {team.get('pointsScored', 0):.1f} ppg")
    except APIError as e:
        print(f"V3 Team Stats: API error - {e}")


def example_with_context_manager():
    """Using the client as a context manager."""
    print("\n--- Context Manager Example ---")
    with EuroleagueClient() as ctx_client:
        clubs = ctx_client.v2.clubs.list(limit=3)
        print(f"Clubs via context manager: {[c.get('name') for c in clubs.get('data', [])]}")


if __name__ == "__main__":
    print("py-euroleague Basic Usage Examples")
    print("=" * 40)

    example_v2_api()
    example_v3_api()
    example_with_context_manager()

    print("\nDone!")
