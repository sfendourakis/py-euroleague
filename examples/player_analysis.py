"""
Player Statistics Analysis Example

This example demonstrates how to:
- Search for players by name
- Get player career statistics and PIR (Performance Index Rating)
- Compare players across different statistical categories
- Analyze player performance trends

PIR (Performance Index Rating) is calculated as:
PIR = (Points + Rebounds + Assists + Steals + Blocks + Fouls Drawn)
    - (Missed FG + Missed FT + Turnovers + Shots Rejected + Fouls Committed)

Reference: https://en.wikipedia.org/wiki/Performance_Index_Rating
"""

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError, NotFoundError


def search_player(client: EuroleagueClient, name: str) -> dict | None:
    """Search for a player by name and return their info."""
    results = client.v2.people.list(search=name, limit=5)
    players = results.get("data", [])

    if not players:
        print(f"No players found matching '{name}'")
        return None

    print(f"Found {len(players)} player(s) matching '{name}':")
    for p in players:
        country_name = p.get("country", {}).get("name", "N/A")
        print(f"  - {p.get('name')} (Code: {p.get('code')}, Country: {country_name})")

    return players[0] if players else None


def get_player_seasons(client: EuroleagueClient, player_code: str) -> list:
    """Get all seasons a player has played."""
    try:
        seasons = client.v2.people.get_seasons(player_code, limit=50)
        return seasons.get("data", [])
    except NotFoundError:
        return []


def get_season_leaders_by_category(
    client: EuroleagueClient, season_code: str, limit: int = 10
) -> dict:
    """Get statistical leaders for a season across all categories."""
    leaders = client.v3.player_stats.leaders(
        competition_code="E", season_mode="Single", season_code=season_code, limit=limit
    )
    return leaders


def display_pir_leaders(leaders: dict, top_n: int = 5):
    """Display PIR (Performance Index Rating) leaders."""
    pir_leaders = leaders.get("pir", [])[:top_n]

    print(f"\nTop {top_n} PIR Leaders:")
    print("-" * 60)
    print(f"{'Rank':<6}{'Player':<30}{'Team':<20}{'PIR':>8}")
    print("-" * 60)

    for player in pir_leaders:
        details = player.get("details", {})
        team = details.get("team", {})
        # Handle multiple teams (player transferred)
        team_name = team.get("name", "N/A").split(";")[0][:18]

        print(
            f"{player.get('rank'):<6}"
            f"{details.get('name', 'N/A'):<30}"
            f"{team_name:<20}"
            f"{player.get('average', 0):>8.1f}"
        )


def display_scoring_leaders(leaders: dict, top_n: int = 5):
    """Display points per game leaders."""
    points_leaders = leaders.get("points", [])[:top_n]

    print(f"\nTop {top_n} Scoring Leaders:")
    print("-" * 60)
    print(f"{'Rank':<6}{'Player':<30}{'Team':<15}{'PPG':>8}")
    print("-" * 60)

    for player in points_leaders:
        details = player.get("details", {})
        team = details.get("team", {})
        team_name = team.get("name", "N/A").split(";")[0][:13]

        print(
            f"{player.get('rank'):<6}"
            f"{details.get('name', 'N/A'):<30}"
            f"{team_name:<15}"
            f"{player.get('average', 0):>8.1f}"
        )


def display_all_statistical_categories(leaders: dict, top_n: int = 3):
    """Display top players in each statistical category."""
    categories = {
        "points": "Points",
        "rebounds": "Rebounds",
        "assists": "Assists",
        "steals": "Steals",
        "blocks": "Blocks",
        "pir": "PIR",
    }

    print("\n" + "=" * 70)
    print("STATISTICAL CATEGORY LEADERS")
    print("=" * 70)

    for key, name in categories.items():
        players = leaders.get(key, [])[:top_n]
        if players:
            print(f"\n{name}:")
            for p in players:
                details = p.get("details", {})
                avg = p.get("average", p.get("value", 0))
                if isinstance(avg, str):
                    print(f"  {p.get('rank')}. {details.get('name', 'N/A')}: {avg}")
                else:
                    print(f"  {p.get('rank')}. {details.get('name', 'N/A')}: {avg:.1f}")


def compare_players(client: EuroleagueClient, player_names: list[str], season_code: str):
    """Compare multiple players' statistics for a season."""
    print(f"\n{'=' * 70}")
    print(f"PLAYER COMPARISON - Season {season_code}")
    print("=" * 70)

    # Get all leaders data
    leaders = get_season_leaders_by_category(client, season_code, limit=100)

    # Find each player in the stats
    for name in player_names:
        print(f"\nSearching for '{name}' in season stats...")

        found = False
        for category, category_data in leaders.items():
            if not isinstance(category_data, list):
                continue
            for player in category_data:
                details = player.get("details", {})
                if name.upper() in details.get("name", "").upper():
                    if not found:
                        print(f"\n  {details.get('name')}:")
                        found = True

                    avg = player.get("average", player.get("value", "N/A"))
                    if isinstance(avg, int | float):
                        print(f"    - {category}: {avg:.1f} (Rank: {player.get('rank')})")
                    else:
                        print(f"    - {category}: {avg} (Rank: {player.get('rank')})")
                    break

        if not found:
            print(f"  Player '{name}' not found in top stats for this season")


def main():
    """Main function demonstrating player analysis capabilities."""
    print("=" * 70)
    print("EUROLEAGUE PLAYER STATISTICS ANALYSIS")
    print("=" * 70)

    with EuroleagueClient() as client:
        # Example 1: Search for a specific player
        print("\n--- Player Search ---")
        player = search_player(client, "Vezenkov")

        if player:
            player_code = player.get("code")
            print(f"\nGetting career history for {player.get('name')}...")
            seasons = get_player_seasons(client, player_code)
            if seasons:
                print(f"Played in {len(seasons)} Euroleague seasons")
                for s in seasons[:5]:
                    print(f"  - {s.get('seasonCode')}: {s.get('clubName', 'N/A')}")

        # Example 2: Get season leaders
        print("\n--- Season Leaders (E2025) ---")
        try:
            leaders = get_season_leaders_by_category(client, "E2025")

            # Display PIR leaders
            display_pir_leaders(leaders)

            # Display scoring leaders
            display_scoring_leaders(leaders)

            # Display all categories
            display_all_statistical_categories(leaders)

        except APIError as e:
            print(f"Error fetching leaders: {e}")

        # Example 3: Compare specific players
        print("\n--- Player Comparison ---")
        players_to_compare = ["Nunn", "Vezenkov", "Tavares"]
        compare_players(client, players_to_compare, "E2025")


if __name__ == "__main__":
    main()
