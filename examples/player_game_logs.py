"""
Player Game Logs Example

This example demonstrates how to:
- Get game-by-game statistics for a specific player
- Track player performance over a season
- Analyze trends and consistency

Note: The API doesn't have a dedicated player game log endpoint,
so we extract player stats from each game's box score.
"""

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError


def get_player_game_logs(
    client: EuroleagueClient,
    player_name: str,
    season_code: str,
    max_games: int = 20,
) -> list[dict]:
    """
    Get game-by-game statistics for a player.

    Args:
        client: EuroleagueClient instance
        player_name: Player name to search for (partial match supported)
        season_code: Season code (e.g., 'E2025')
        max_games: Maximum number of games to fetch

    Returns:
        List of game log dictionaries with player stats
    """
    # Get games for the season (need limit=400 to get all games including completed ones)
    games = client.v2.games.list("E", season_code, limit=400)
    game_logs = []

    for game_data in games.get("data", []):
        game_code = game_data.get("gameCode")
        if not game_code:
            continue

        # Only process played games
        if not game_data.get("played", False):
            continue

        # Get game stats
        try:
            stats = client.v3.stats.get_game_stats("E", season_code, game_code)
        except APIError:
            continue

        # Search for player in both teams
        for team_key in ["local", "road"]:
            team = stats.get(team_key, {})
            opponent_key = "road" if team_key == "local" else "local"
            opponent_team = stats.get(opponent_key, {})

            for player in team.get("players", []):
                player_info = player.get("player", {}).get("person", {})
                if player_name.upper() in player_info.get("name", "").upper():
                    player_stats = player.get("stats", {})

                    # Get opponent name
                    opponent_players = opponent_team.get("players", [])
                    opponent_name = "N/A"
                    if opponent_players:
                        opp_club = opponent_players[0].get("player", {}).get("club", {})
                        opponent_name = opp_club.get("abbreviatedName", opp_club.get("name", "N/A"))

                    # Get game result
                    local_score = game_data.get("local", {}).get("score", 0)
                    road_score = game_data.get("road", {}).get("score", 0)
                    if team_key == "local":
                        result = "W" if local_score > road_score else "L"
                        team_score = local_score
                        opp_score = road_score
                    else:
                        result = "W" if road_score > local_score else "L"
                        team_score = road_score
                        opp_score = local_score

                    game_logs.append(
                        {
                            "date": game_data.get("date", "")[:10],
                            "round": game_data.get("round"),
                            "opponent": opponent_name,
                            "home_away": "H" if team_key == "local" else "A",
                            "result": result,
                            "score": f"{team_score}-{opp_score}",
                            "minutes": player_stats.get("timePlayed", 0) / 60,
                            "points": player_stats.get("points", 0),
                            "fg2m": player_stats.get("fieldGoalsMade2", 0),
                            "fg2a": player_stats.get("fieldGoalsAttempted2", 0),
                            "fg3m": player_stats.get("fieldGoalsMade3", 0),
                            "fg3a": player_stats.get("fieldGoalsAttempted3", 0),
                            "ftm": player_stats.get("freeThrowsMade", 0),
                            "fta": player_stats.get("freeThrowsAttempted", 0),
                            "rebounds": player_stats.get("totalRebounds", 0),
                            "offensive_reb": player_stats.get("offensiveRebounds", 0),
                            "defensive_reb": player_stats.get("defensiveRebounds", 0),
                            "assists": player_stats.get("assistances", 0),
                            "steals": player_stats.get("steals", 0),
                            "blocks": player_stats.get("blocksFavour", 0),
                            "turnovers": player_stats.get("turnovers", 0),
                            "fouls": player_stats.get("foulsCommited", 0),
                            "plus_minus": player_stats.get("plusMinus", 0),
                            "pir": player_stats.get("valuation", 0),
                        }
                    )

        if len(game_logs) >= max_games:
            break

    return game_logs


def display_game_logs(game_logs: list[dict], player_name: str):
    """Display game logs in a formatted table."""
    if not game_logs:
        print(f"No game logs found for {player_name}")
        return

    print(f"\n{'=' * 110}")
    print(f"{player_name.upper()} - GAME LOG ({len(game_logs)} games)")
    print("=" * 110)

    # Header
    print(
        f"{'Date':<12}{'Rd':>4}{'Opp':>12}{'H/A':>5}{'W/L':>5}"
        f"{'MIN':>6}{'PTS':>5}{'REB':>5}{'AST':>5}{'STL':>5}{'BLK':>5}{'TO':>5}{'PIR':>6}"
    )
    print("-" * 110)

    # Game rows
    for log in game_logs:
        print(
            f"{log['date']:<12}"
            f"{log['round']:>4}"
            f"{log['opponent'][:10]:>12}"
            f"{log['home_away']:>5}"
            f"{log['result']:>5}"
            f"{log['minutes']:>6.0f}"
            f"{log['points']:>5.0f}"
            f"{log['rebounds']:>5.0f}"
            f"{log['assists']:>5.0f}"
            f"{log['steals']:>5.0f}"
            f"{log['blocks']:>5.0f}"
            f"{log['turnovers']:>5.0f}"
            f"{log['pir']:>6.0f}"
        )


def display_detailed_game_logs(game_logs: list[dict], player_name: str):
    """Display detailed shooting splits for each game."""
    if not game_logs:
        return

    print(f"\n{'=' * 100}")
    print(f"{player_name.upper()} - SHOOTING SPLITS")
    print("=" * 100)

    print(
        f"{'Date':<12}{'Opp':>10}{'PTS':>5}"
        f"{'2PM-A':>10}{'2P%':>7}"
        f"{'3PM-A':>10}{'3P%':>7}"
        f"{'FTM-A':>10}{'FT%':>7}"
    )
    print("-" * 100)

    for log in game_logs:
        fg2_pct = (log["fg2m"] / log["fg2a"] * 100) if log["fg2a"] > 0 else 0
        fg3_pct = (log["fg3m"] / log["fg3a"] * 100) if log["fg3a"] > 0 else 0
        ft_pct = (log["ftm"] / log["fta"] * 100) if log["fta"] > 0 else 0

        fg2_str = f"{int(log['fg2m'])}-{int(log['fg2a'])}"
        fg3_str = f"{int(log['fg3m'])}-{int(log['fg3a'])}"
        ft_str = f"{int(log['ftm'])}-{int(log['fta'])}"

        print(
            f"{log['date']:<12}"
            f"{log['opponent'][:10]:>10}"
            f"{log['points']:>5.0f}"
            f"{fg2_str:>10}"
            f"{fg2_pct:>6.1f}%"
            f"{fg3_str:>10}"
            f"{fg3_pct:>6.1f}%"
            f"{ft_str:>10}"
            f"{ft_pct:>6.1f}%"
        )


def calculate_averages(game_logs: list[dict]) -> dict:
    """Calculate season averages from game logs."""
    if not game_logs:
        return {}

    n = len(game_logs)
    return {
        "games": n,
        "minutes": sum(g["minutes"] for g in game_logs) / n,
        "points": sum(g["points"] for g in game_logs) / n,
        "rebounds": sum(g["rebounds"] for g in game_logs) / n,
        "assists": sum(g["assists"] for g in game_logs) / n,
        "steals": sum(g["steals"] for g in game_logs) / n,
        "blocks": sum(g["blocks"] for g in game_logs) / n,
        "turnovers": sum(g["turnovers"] for g in game_logs) / n,
        "pir": sum(g["pir"] for g in game_logs) / n,
        "fg2_pct": sum(g["fg2m"] for g in game_logs)
        / max(sum(g["fg2a"] for g in game_logs), 1)
        * 100,
        "fg3_pct": sum(g["fg3m"] for g in game_logs)
        / max(sum(g["fg3a"] for g in game_logs), 1)
        * 100,
        "ft_pct": sum(g["ftm"] for g in game_logs) / max(sum(g["fta"] for g in game_logs), 1) * 100,
    }


def display_season_averages(averages: dict, player_name: str):
    """Display season averages summary."""
    if not averages:
        return

    print(f"\n{'=' * 60}")
    print(f"{player_name.upper()} - SEASON AVERAGES ({averages['games']} games)")
    print("=" * 60)

    print(f"  Minutes:    {averages['minutes']:.1f}")
    print(f"  Points:     {averages['points']:.1f}")
    print(f"  Rebounds:   {averages['rebounds']:.1f}")
    print(f"  Assists:    {averages['assists']:.1f}")
    print(f"  Steals:     {averages['steals']:.1f}")
    print(f"  Blocks:     {averages['blocks']:.1f}")
    print(f"  Turnovers:  {averages['turnovers']:.1f}")
    print(f"  PIR:        {averages['pir']:.1f}")
    print(f"\n  2P%:        {averages['fg2_pct']:.1f}%")
    print(f"  3P%:        {averages['fg3_pct']:.1f}%")
    print(f"  FT%:        {averages['ft_pct']:.1f}%")


def main():
    """Main function demonstrating player game logs."""
    print("=" * 60)
    print("EUROLEAGUE PLAYER GAME LOGS")
    print("=" * 60)

    with EuroleagueClient() as client:
        season_code = "E2025"

        # Example 1: Get game logs for a star player
        player_name = "Vezenkov"
        print(f"\nFetching game logs for {player_name}...")
        print("(This may take a moment as we fetch stats from each game)")

        game_logs = get_player_game_logs(client, player_name, season_code, max_games=15)

        # Display game logs
        display_game_logs(game_logs, player_name)

        # Display shooting splits
        display_detailed_game_logs(game_logs, player_name)

        # Calculate and display averages
        averages = calculate_averages(game_logs)
        display_season_averages(averages, player_name)

        # Example 2: Compare another player
        print("\n" + "=" * 60)
        player_name2 = "Nunn"
        print(f"\nFetching game logs for {player_name2}...")

        game_logs2 = get_player_game_logs(client, player_name2, season_code, max_games=10)
        display_game_logs(game_logs2, player_name2)

        averages2 = calculate_averages(game_logs2)
        display_season_averages(averages2, player_name2)


if __name__ == "__main__":
    main()
