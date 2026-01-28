"""
Fantasy Basketball Analysis Example

This example demonstrates how to:
- Identify top fantasy performers using PIR
- Find value picks (high performance, potentially overlooked)
- Analyze player consistency
- Build optimal fantasy lineups

Fantasy Euroleague typically uses PIR as the main scoring metric.
Reference: https://medium.com/@dogacandu/how-i-analyze-fantasy-euroleague-basketball-data-and-predict-player-price-25f346867835
"""

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError


def get_all_statistical_leaders(client: EuroleagueClient, season_code: str) -> dict:
    """Get comprehensive player statistics for fantasy analysis."""
    return client.v3.player_stats.leaders(
        competition_code="E",
        season_mode="Single",
        season_code=season_code,
        limit=50  # Get more players for better analysis
    )


def calculate_fantasy_score(player_stats: dict) -> float:
    """
    Calculate estimated fantasy score based on available stats.
    In Euroleague Fantasy, PIR is the primary scoring metric.
    """
    return player_stats.get("average", 0)


def display_top_fantasy_performers(leaders: dict, category: str = "pir", top_n: int = 15):
    """Display top fantasy performers by specified category."""
    players = leaders.get(category, [])[:top_n]

    print(f"\n{'=' * 80}")
    print(f"TOP {top_n} FANTASY PERFORMERS BY {category.upper()}")
    print("=" * 80)
    print(f"{'Rank':<6}{'Player':<30}{'Team':<20}{'Avg':>10}{'GP':>8}")
    print("-" * 74)

    for player in players:
        details = player.get("details", {})
        team = details.get("team", {})
        team_name = team.get("name", "N/A").split(";")[0][:18]

        avg = player.get("average", player.get("value", 0))
        gp = player.get("gamesPlayed", "N/A")

        if isinstance(avg, str):
            avg_str = avg
        else:
            avg_str = f"{avg:.1f}"

        print(f"{player.get('rank'):<6}"
              f"{details.get('name', 'N/A'):<30}"
              f"{team_name:<20}"
              f"{avg_str:>10}"
              f"{gp:>8}")


def find_value_picks(leaders: dict, min_games: int = 15) -> list:
    """
    Find value picks - players with good PIR who might be undervalued.
    These are players with solid stats who may not be in the top 10.
    """
    pir_players = leaders.get("pir", [])
    value_picks = []

    # Look at players ranked 10-30 in PIR
    for player in pir_players[9:30]:
        gp = player.get("gamesPlayed", 0)
        if gp >= min_games:
            value_picks.append(player)

    return value_picks


def display_value_picks(value_picks: list):
    """Display value picks for fantasy."""
    print(f"\n{'=' * 80}")
    print("VALUE PICKS (Solid performers outside top 10)")
    print("=" * 80)
    print(f"{'Rank':<6}{'Player':<30}{'Team':<20}{'PIR':>10}{'GP':>8}")
    print("-" * 74)

    for player in value_picks[:10]:
        details = player.get("details", {})
        team = details.get("team", {})
        team_name = team.get("name", "N/A").split(";")[0][:18]

        print(f"{player.get('rank'):<6}"
              f"{details.get('name', 'N/A'):<30}"
              f"{team_name:<20}"
              f"{player.get('average', 0):>10.1f}"
              f"{player.get('gamesPlayed', 0):>8}")


def analyze_category_specialists(leaders: dict):
    """Find category specialists - players who excel in specific stats."""
    categories = {
        "points": "Scorers",
        "rebounds": "Rebounders",
        "assists": "Playmakers",
        "steals": "Defensive Specialists",
        "blocks": "Shot Blockers",
        "threePointersPercentage": "3PT Shooters",
    }

    print(f"\n{'=' * 80}")
    print("CATEGORY SPECIALISTS")
    print("=" * 80)

    for cat_key, cat_name in categories.items():
        players = leaders.get(cat_key, [])[:3]
        if players:
            print(f"\nTop {cat_name}:")
            for p in players:
                details = p.get("details", {})
                avg = p.get("average", p.get("value", "N/A"))
                if isinstance(avg, (int, float)):
                    print(f"  {p.get('rank')}. {details.get('name', 'N/A')}: {avg:.1f}")
                else:
                    print(f"  {p.get('rank')}. {details.get('name', 'N/A')}: {avg}")


def build_fantasy_roster(leaders: dict) -> dict:
    """
    Build an optimal fantasy roster based on PIR.
    Typical fantasy roster: 2 Guards, 2 Forwards, 1 Center, 3 Flex
    """
    pir_players = leaders.get("pir", [])

    roster = {
        "guards": [],
        "forwards": [],
        "centers": [],
        "flex": []
    }

    for player in pir_players:
        details = player.get("details", {})
        position = details.get("position", "").lower()

        player_info = {
            "name": details.get("name"),
            "team": details.get("team", {}).get("name", "").split(";")[0],
            "position": position,
            "pir": player.get("average", 0),
            "rank": player.get("rank")
        }

        if "guard" in position and len(roster["guards"]) < 2:
            roster["guards"].append(player_info)
        elif "forward" in position and len(roster["forwards"]) < 2:
            roster["forwards"].append(player_info)
        elif "center" in position and len(roster["centers"]) < 1:
            roster["centers"].append(player_info)
        elif len(roster["flex"]) < 3:
            roster["flex"].append(player_info)

    return roster


def display_fantasy_roster(roster: dict):
    """Display the built fantasy roster."""
    print(f"\n{'=' * 80}")
    print("OPTIMAL FANTASY ROSTER (Based on PIR)")
    print("=" * 80)

    total_pir = 0

    for position, players in roster.items():
        print(f"\n{position.upper()}:")
        for p in players:
            print(f"  - {p['name']} ({p['team'][:15]}) - PIR: {p['pir']:.1f}")
            total_pir += p['pir']

    filled_spots = sum(len(p) for p in roster.values())
    print(f"\n{'=' * 40}")
    print(f"Roster spots filled: {filled_spots}/8")
    print(f"Total projected PIR: {total_pir:.1f}")
    print(f"Average PIR per player: {total_pir/filled_spots:.1f}" if filled_spots > 0 else "")


def weekly_hot_picks(leaders: dict, top_n: int = 5):
    """Identify players who are currently performing well."""
    print(f"\n{'=' * 80}")
    print("HOT PICKS - Top Performers to Consider")
    print("=" * 80)

    pir_leaders = leaders.get("pir", [])[:top_n]
    points_leaders = leaders.get("points", [])[:top_n]

    print("\nTop PIR (Overall Fantasy Value):")
    for p in pir_leaders:
        details = p.get("details", {})
        print(f"  {p.get('rank')}. {details.get('name')} - {p.get('average', 0):.1f} PIR")

    print("\nTop Scorers (High Ceiling):")
    for p in points_leaders:
        details = p.get("details", {})
        print(f"  {p.get('rank')}. {details.get('name')} - {p.get('average', 0):.1f} PPG")


def main():
    """Main function demonstrating fantasy basketball analysis."""
    print("=" * 80)
    print("EUROLEAGUE FANTASY BASKETBALL ANALYSIS")
    print("=" * 80)

    with EuroleagueClient() as client:
        season_code = "E2025"

        print(f"\nAnalyzing season {season_code}...")

        # Get comprehensive stats
        leaders = get_all_statistical_leaders(client, season_code)

        # Top fantasy performers by PIR
        display_top_fantasy_performers(leaders, "pir", top_n=15)

        # Top scorers
        display_top_fantasy_performers(leaders, "points", top_n=10)

        # Value picks
        value_picks = find_value_picks(leaders)
        display_value_picks(value_picks)

        # Category specialists
        analyze_category_specialists(leaders)

        # Build optimal roster
        roster = build_fantasy_roster(leaders)
        display_fantasy_roster(roster)

        # Hot picks
        weekly_hot_picks(leaders)


if __name__ == "__main__":
    main()
