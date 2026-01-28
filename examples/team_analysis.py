"""
Team Statistics Analysis Example

This example demonstrates how to:
- Get team standings and rankings
- Analyze offensive and defensive ratings
- Compare teams across statistical categories
- Track team performance metrics

Key metrics explained:
- Offensive Rating: Points scored per 100 possessions
- Defensive Rating: Points allowed per 100 possessions
- Net Rating: Offensive Rating - Defensive Rating
- PIR: Team Performance Index Rating
"""

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError


def get_team_standings(client: EuroleagueClient, season_code: str) -> list:
    """Get team standings for a season."""
    stats = client.v3.team_stats.traditional(
        competition_code="E",
        season_mode="Single",
        season_code=season_code
    )
    return stats.get("teams", [])


def display_offensive_rankings(teams: list, top_n: int = 10):
    """Display teams ranked by offensive performance (points per game)."""
    # Sort by points scored
    sorted_teams = sorted(
        teams,
        key=lambda t: t.get("pointsScored", 0),
        reverse=True
    )[:top_n]

    print(f"\nTop {top_n} Offensive Teams (Points Per Game):")
    print("-" * 70)
    print(f"{'Rank':<6}{'Team':<35}{'PPG':>10}{'FG%':>10}{'3P%':>10}")
    print("-" * 70)

    for i, team in enumerate(sorted_teams, 1):
        team_info = team.get("team", {})
        name = team_info.get("name", "N/A")[:33]

        # Parse percentage strings
        fg_pct = team.get("twoPointersPercentage", "0%")
        three_pct = team.get("threePointersPercentage", "0%")

        print(f"{i:<6}"
              f"{name:<35}"
              f"{team.get('pointsScored', 0):>10.1f}"
              f"{fg_pct:>10}"
              f"{three_pct:>10}")


def display_defensive_rankings(teams: list, top_n: int = 10):
    """Display teams ranked by defensive performance."""
    # For defense, we'd need opponent stats - let's show rebounds and blocks
    sorted_teams = sorted(
        teams,
        key=lambda t: t.get("totalRebounds", 0),
        reverse=True
    )[:top_n]

    print(f"\nTop {top_n} Rebounding Teams:")
    print("-" * 70)
    print(f"{'Rank':<6}{'Team':<35}{'REB':>10}{'OREB':>10}{'DREB':>10}")
    print("-" * 70)

    for i, team in enumerate(sorted_teams, 1):
        team_info = team.get("team", {})
        name = team_info.get("name", "N/A")[:33]

        print(f"{i:<6}"
              f"{name:<35}"
              f"{team.get('totalRebounds', 0):>10.1f}"
              f"{team.get('offensiveRebounds', 0):>10.1f}"
              f"{team.get('defensiveRebounds', 0):>10.1f}")


def display_efficiency_rankings(teams: list, top_n: int = 10):
    """Display teams ranked by overall efficiency (PIR)."""
    sorted_teams = sorted(
        teams,
        key=lambda t: t.get("pir", 0),
        reverse=True
    )[:top_n]

    print(f"\nTop {top_n} Teams by PIR (Performance Index Rating):")
    print("-" * 80)
    print(f"{'Rank':<6}{'Team':<35}{'PIR':>10}{'AST':>10}{'STL':>10}{'BLK':>10}")
    print("-" * 80)

    for i, team in enumerate(sorted_teams, 1):
        team_info = team.get("team", {})
        name = team_info.get("name", "N/A")[:33]

        print(f"{i:<6}"
              f"{name:<35}"
              f"{team.get('pir', 0):>10.1f}"
              f"{team.get('assists', 0):>10.1f}"
              f"{team.get('steals', 0):>10.1f}"
              f"{team.get('blocks', 0):>10.1f}")


def display_team_profile(client: EuroleagueClient, team_code: str, season_code: str):
    """Display detailed profile for a specific team."""
    print(f"\n{'=' * 70}")
    print(f"TEAM PROFILE: {team_code}")
    print("=" * 70)

    try:
        # Get club info
        club = client.v2.clubs.get(team_code)
        print(f"\nClub: {club.get('name', 'N/A')}")
        print(f"Country: {club.get('country', {}).get('name', 'N/A')}")
        if club.get("venue"):
            print(f"Venue: {club.get('venue', {}).get('name', 'N/A')} "
                  f"(Capacity: {club.get('venue', {}).get('capacity', 'N/A')})")

        # Get team stats for season
        stats = client.v3.stats.get_club_stats("E", season_code, team_code)

        if stats:
            print(f"\nSeason {season_code} Statistics:")
            print("-" * 40)

            # API returns a list with accumulated and averagePerGame stats
            if isinstance(stats, list) and len(stats) > 0:
                avg_stats = stats[0].get("averagePerGame", {})
                print(f"  Games Played: {stats[0].get('accumulated', {}).get('gamesPlayed', 'N/A')}")
                print(f"  Points/Game: {avg_stats.get('points', 0):.1f}")
                print(f"  Rebounds/Game: {avg_stats.get('totalRebounds', 0):.1f}")
                print(f"  Assists/Game: {avg_stats.get('assistances', 0):.1f}")
                print(f"  PIR/Game: {avg_stats.get('valuation', 0):.1f}")

    except APIError as e:
        print(f"Error: {e}")


def compare_teams(teams: list, team_codes: list[str]):
    """Compare specific teams side by side."""
    print(f"\n{'=' * 80}")
    print("TEAM COMPARISON")
    print("=" * 80)

    # Find the teams
    selected_teams = []
    for code in team_codes:
        for team in teams:
            team_info = team.get("team", {})
            if code.upper() in team_info.get("code", "").upper():
                selected_teams.append(team)
                break

    if not selected_teams:
        print("No matching teams found")
        return

    # Headers
    print(f"\n{'Statistic':<25}", end="")
    for team in selected_teams:
        name = team.get("team", {}).get("name", "N/A")[:15]
        print(f"{name:>18}", end="")
    print()
    print("-" * (25 + 18 * len(selected_teams)))

    # Stats to compare
    stats_to_show = [
        ("pointsScored", "Points/Game"),
        ("totalRebounds", "Rebounds/Game"),
        ("assists", "Assists/Game"),
        ("steals", "Steals/Game"),
        ("blocks", "Blocks/Game"),
        ("turnovers", "Turnovers/Game"),
        ("pir", "PIR"),
        ("twoPointersPercentage", "2P%"),
        ("threePointersPercentage", "3P%"),
        ("freeThrowsPercentage", "FT%"),
    ]

    for stat_key, stat_name in stats_to_show:
        print(f"{stat_name:<25}", end="")
        for team in selected_teams:
            value = team.get(stat_key, 0)
            if isinstance(value, str):
                print(f"{value:>18}", end="")
            else:
                print(f"{value:>18.1f}", end="")
        print()


def main():
    """Main function demonstrating team analysis capabilities."""
    print("=" * 70)
    print("EUROLEAGUE TEAM STATISTICS ANALYSIS")
    print("=" * 70)

    with EuroleagueClient() as client:
        season_code = "E2025"

        # Get all team stats for the season
        print(f"\nFetching team statistics for season {season_code}...")
        teams = get_team_standings(client, season_code)
        print(f"Found {len(teams)} teams")

        # Display offensive rankings
        display_offensive_rankings(teams)

        # Display rebounding rankings
        display_defensive_rankings(teams)

        # Display efficiency rankings
        display_efficiency_rankings(teams)

        # Compare specific teams
        print("\n--- Team Comparison: Top Contenders ---")
        compare_teams(teams, ["OLY", "PAN", "MAD", "BAR"])

        # Display detailed profile for a team
        display_team_profile(client, "OLY", season_code)


if __name__ == "__main__":
    main()
