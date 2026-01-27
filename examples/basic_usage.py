"""Basic usage example for py-euroleague."""

from euroleague import EuroleagueClient
from euroleague.auth import TokenInfo

# Initialize the client
client = EuroleagueClient(client_id="your_client_id")

# Option 1: OAuth2 PKCE Authentication Flow
# -----------------------------------------
# Step 1: Generate authorization URL
auth_url, state, verifier = client.get_authorization_url()
print(f"Please visit this URL to authorize: {auth_url}")
print(f"State: {state}")
print(f"Save this verifier: {verifier}")

# Step 2: After user authorizes and is redirected, exchange the code
# The authorization code comes from the redirect URL query parameter
# auth_code = "code_from_redirect_url"
# client.authenticate(code=auth_code, code_verifier=verifier)


# Option 2: Use a pre-obtained token
# ----------------------------------
# If you already have an access token, you can set it directly:
# client.set_token(TokenInfo(
#     access_token="your_access_token",
#     token_type="Bearer",
#     expires_in=3600
# ))


# Example API calls (requires authentication)
# -------------------------------------------

def example_v1_api():
    """V1 API examples (legacy/simple endpoints)."""
    # Get standings for a season
    standings = client.v1.standings.get(season_code="E2024")
    print("V1 Standings:", standings)

    # Get game box score
    box_score = client.v1.games.get(season_code="E2024", game_code=1)
    print("V1 Box Score:", box_score)

    # Get teams with rosters
    teams = client.v1.teams.get(season_code="E2024")
    print("V1 Teams:", teams)


def example_v2_api():
    """V2 API examples (comprehensive endpoints)."""
    # List all clubs
    clubs = client.v2.clubs.list(limit=10)
    print("V2 Clubs:", clubs)

    # Get specific club
    barcelona = client.v2.clubs.get("BAR")
    print("V2 Barcelona:", barcelona)

    # List competitions
    competitions = client.v2.competitions.list()
    print("V2 Competitions:", competitions)

    # Get games for a season
    games = client.v2.games.list(
        competition_code="E",
        season_code="2024",
        limit=10
    )
    print("V2 Games:", games)

    # Get people (players, coaches)
    people = client.v2.people.list(search="Doncic", limit=5)
    print("V2 People search:", people)

    # Get season standings
    standings = client.v2.standings.get_round(
        competition_code="E",
        season_code="2024",
        round_number=10
    )
    print("V2 Standings:", standings)


def example_v3_api():
    """V3 API examples (statistics-focused endpoints)."""
    # Get player leaders
    leaders = client.v3.player_stats.leaders(
        competition_code="E",
        season_code="2024",
        limit=10
    )
    print("V3 Player Leaders:", leaders)

    # Get traditional player stats
    traditional = client.v3.player_stats.traditional(
        competition_code="E",
        season_code="2024",
        limit=10
    )
    print("V3 Traditional Stats:", traditional)

    # Get advanced player stats
    advanced = client.v3.player_stats.advanced(
        competition_code="E",
        season_code="2024",
        limit=10
    )
    print("V3 Advanced Stats:", advanced)

    # Get team stats
    team_stats = client.v3.team_stats.traditional(
        competition_code="E",
        season_code="2024"
    )
    print("V3 Team Stats:", team_stats)

    # Get various standings views
    basic_standings = client.v3.standings.basic("E", "2024", 10)
    streaks = client.v3.standings.streaks("E", "2024", 10)
    margins = client.v3.standings.margins("E", "2024", 10)
    print("V3 Basic Standings:", basic_standings)
    print("V3 Streaks:", streaks)
    print("V3 Margins:", margins)


# Context manager usage
def example_with_context_manager():
    """Using the client as a context manager."""
    with EuroleagueClient(client_id="your_client_id") as client:
        # Client is automatically closed when exiting the context
        clubs = client.v2.clubs.list()
        print("Clubs:", clubs)


if __name__ == "__main__":
    print("py-euroleague Basic Usage Examples")
    print("=" * 40)
    print("\nNote: You need to authenticate before making API calls.")
    print("See the authentication examples above.")

    # Uncomment to run examples after authentication:
    # example_v1_api()
    # example_v2_api()
    # example_v3_api()
