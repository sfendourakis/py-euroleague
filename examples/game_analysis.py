"""
Game Analysis Example

This example demonstrates how to:
- Get game schedules and results
- Analyze box scores and game statistics
- Get head-to-head history between teams
- Compare team matchups
"""

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError


def get_recent_games(client: EuroleagueClient, season_code: str, limit: int = 200) -> list:
    """Get recent games for a season (fetches more to include completed games)."""
    games = client.v2.games.list(competition_code="E", season_code=season_code, limit=limit)
    # V2 API uses local/road instead of homeClub/awayClub - normalize in analyze_round
    # Return raw data here since it's used before normalize_games is defined
    return games.get("data", [])


def display_game_schedule(games: list, title: str = "Recent Games"):
    """Display game schedule with scores."""
    print(f"\n{title}:")
    print("-" * 80)
    print(f"{'Round':<8}{'Date':<12}{'Home Team':<25}{'Score':^15}{'Away Team':<25}")
    print("-" * 80)

    for game in games:
        home = game.get("homeClub", {})
        away = game.get("awayClub", {})

        home_name = home.get("name", "TBD")[:23]
        away_name = away.get("name", "TBD")[:23]

        home_score = game.get("homeScore", "-")
        away_score = game.get("awayScore", "-")
        score = f"{home_score} - {away_score}" if home_score != "-" else "vs"

        game_date = game.get("date", "TBD")[:10]
        round_num = game.get("round", "")

        print(
            f"{round_num:<8}"
            f"{game_date:<12}"
            f"{home_name:<25}"
            f"{score:^15}"
            f"{away_name:<25}"
        )


def get_game_stats(client: EuroleagueClient, season_code: str, game_code: int) -> dict:
    """Get detailed statistics for a specific game."""
    try:
        stats = client.v3.stats.get_game_stats("E", season_code, game_code)
        return stats
    except APIError as e:
        print(f"Error getting game stats: {e}")
        return {}


def display_game_box_score(stats: dict):
    """Display box score for a game."""
    if not stats:
        print("No stats available")
        return

    # V3 API uses local/road with total for team stats
    local = stats.get("local", {})
    road = stats.get("road", {})

    print(f"\n{'=' * 80}")
    print("GAME BOX SCORE")
    print("=" * 80)

    # Get team names from player data if available
    local_players = local.get("players", [])
    road_players = road.get("players", [])

    home_name = "Home"
    away_name = "Away"
    if local_players:
        club = local_players[0].get("player", {}).get("club", {})
        home_name = club.get("abbreviatedName", club.get("name", "Home"))
    if road_players:
        club = road_players[0].get("player", {}).get("club", {})
        away_name = club.get("abbreviatedName", club.get("name", "Away"))

    print(f"\n{home_name} vs {away_name}")
    print("-" * 60)

    # Get totals
    home_total = local.get("total", {})
    away_total = road.get("total", {})

    # Stats comparison - V3 uses different key names
    stats_to_show = [
        ("points", "Points"),
        ("fieldGoalsMade2", "2PT Made"),
        ("fieldGoalsAttempted2", "2PT Attempted"),
        ("fieldGoalsMade3", "3PT Made"),
        ("fieldGoalsAttempted3", "3PT Attempted"),
        ("freeThrowsMade", "FT Made"),
        ("freeThrowsAttempted", "FT Attempted"),
        ("totalRebounds", "Rebounds"),
        ("offensiveRebounds", "Offensive Reb"),
        ("defensiveRebounds", "Defensive Reb"),
        ("assistances", "Assists"),
        ("steals", "Steals"),
        ("turnovers", "Turnovers"),
        ("blocksFavour", "Blocks"),
        ("foulsCommited", "Fouls"),
        ("valuation", "PIR"),
    ]

    print(f"{'Stat':<25}{home_name[:15]:>15}{away_name[:15]:>15}")
    print("-" * 55)

    for stat_key, stat_name in stats_to_show:
        home_val = home_total.get(stat_key, 0)
        away_val = away_total.get(stat_key, 0)
        if isinstance(home_val, float):
            print(f"{stat_name:<25}{home_val:>15.0f}{away_val:>15.0f}")
        else:
            print(f"{stat_name:<25}{home_val:>15}{away_val:>15}")


def get_head_to_head(client: EuroleagueClient, season_code: str, game_code: int) -> dict:
    """Get head-to-head history for a matchup."""
    try:
        history = client.v2.games.get_history("E", season_code, game_code)
        return history
    except APIError as e:
        print(f"Error getting head-to-head: {e}")
        return {}


def display_head_to_head(history: dict):
    """Display head-to-head statistics."""
    if not history:
        print("No history available")
        return

    print(f"\n{'=' * 70}")
    print("HEAD-TO-HEAD HISTORY")
    print("=" * 70)

    # Get team names from the matchup
    local_club = history.get("localClub", {}).get("club", {})
    road_club = history.get("roadClub", {}).get("club", {})
    local_name = local_club.get("abbreviatedName", local_club.get("name", "Home"))
    road_name = road_club.get("abbreviatedName", road_club.get("name", "Away"))

    # Show records
    records = history.get("records", {})
    if records:
        local_wins = records.get("localWins", 0)
        road_wins = records.get("roadWins", 0)
        print(f"\nAll-time record: {local_name} {local_wins} - {road_wins} {road_name}")

    games = history.get("games", [])
    if games:
        print(f"\nLast {min(5, len(games))} meetings:")
        print("-" * 70)

        for game in games[:5]:
            # Games use local/road structure
            local = game.get("local", {})
            road = game.get("road", {})
            local_score = local.get("score", 0)
            road_score = road.get("score", 0)
            score = f"{local_score}-{road_score}"
            date = game.get("date", "N/A")[:10]
            season = game.get("season", {}).get("alias", "N/A")

            print(f"  {date} ({season}): {local_name} {score} {road_name}")


def get_team_comparison(client: EuroleagueClient, season_code: str, game_code: int) -> dict:
    """Get pre-game team comparison."""
    try:
        comparison = client.v3.stats.get_teams_comparison("E", season_code, game_code)
        return comparison
    except APIError as e:
        print(f"Error getting team comparison: {e}")
        return {}


def display_team_comparison(comparison: dict):
    """Display team comparison for a matchup."""
    if not comparison:
        print("No comparison data available")
        return

    print(f"\n{'=' * 70}")
    print("PRE-GAME TEAM COMPARISON")
    print("=" * 70)

    home = comparison.get("homeClub", {})
    away = comparison.get("awayClub", {})

    home_name = home.get("name", "Home Team")
    away_name = away.get("name", "Away Team")

    print(f"\n{home_name} vs {away_name}")


def normalize_games(games_data: list) -> list:
    """Normalize V2 games API response to consistent format."""
    normalized = []
    for game in games_data:
        local = game.get("local", {})
        road = game.get("road", {})
        normalized.append(
            {
                "gameCode": game.get("gameCode"),
                "round": game.get("round"),
                "date": game.get("date"),
                "homeClub": local.get("club", {}),
                "awayClub": road.get("club", {}),
                "homeScore": local.get("score"),
                "awayScore": road.get("score"),
                "played": game.get("played"),
            }
        )
    return normalized


def analyze_round(client: EuroleagueClient, season_code: str, round_number: int):
    """Analyze all games in a specific round."""
    print(f"\n{'=' * 70}")
    print(f"ROUND {round_number} ANALYSIS")
    print("=" * 70)

    games = client.v2.games.list(
        competition_code="E", season_code=season_code, round_number=round_number, limit=20
    )

    game_list = normalize_games(games.get("data", []))
    if not game_list:
        print(f"No games found for round {round_number}")
        return

    display_game_schedule(game_list, f"Round {round_number} Games")

    # Analyze completed games
    completed = [g for g in game_list if g.get("played")]
    if completed:
        print(f"\n{len(completed)} games completed")

        # Calculate average scores
        home_wins = sum(
            1 for g in completed if (g.get("homeScore", 0) or 0) > (g.get("awayScore", 0) or 0)
        )
        away_wins = len(completed) - home_wins

        print(f"Home wins: {home_wins}, Away wins: {away_wins}")


def main():
    """Main function demonstrating game analysis capabilities."""
    print("=" * 70)
    print("EUROLEAGUE GAME ANALYSIS")
    print("=" * 70)

    with EuroleagueClient() as client:
        season_code = "E2025"  # Season code format

        # Get recent games (fetch more to include completed games)
        print("\n--- Recent Games ---")
        raw_games = get_recent_games(client, season_code)
        games = normalize_games(raw_games)
        # Display only the first 10 completed games
        completed_for_display = [g for g in games if g.get("played")][:10]
        display_game_schedule(completed_for_display)

        # Analyze a specific round
        analyze_round(client, season_code, round_number=20)

        # Find a completed game to analyze (skip future games)
        completed_games = [g for g in games if g.get("played")]
        if completed_games:
            first_game = completed_games[0]
            game_code = first_game.get("gameCode")

            if game_code:
                print(f"\n--- Analyzing Game {game_code} ---")
                print(
                    f"{first_game.get('homeClub', {}).get('name')} vs "
                    f"{first_game.get('awayClub', {}).get('name')}"
                )

                # Get game stats
                stats = get_game_stats(client, season_code, game_code)
                display_game_box_score(stats)

                # Get head-to-head
                history = get_head_to_head(client, season_code, game_code)
                display_head_to_head(history)


if __name__ == "__main__":
    main()
