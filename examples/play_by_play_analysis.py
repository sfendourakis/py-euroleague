"""
Play-by-Play Analysis Example

This example demonstrates how to:
- Fetch play-by-play data for a game
- Analyze scoring patterns and runs
- Track player performance throughout a game
- Calculate shot statistics from play-by-play data
"""

from collections import defaultdict

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError
from euroleague.models.live.play_by_play import PlayByPlayResponse


def get_play_by_play(
    client: EuroleagueClient, season_code: str, game_code: int
) -> PlayByPlayResponse | None:
    """Get play-by-play data for a game."""
    try:
        pbp = client.live.play_by_play.get(season_code, game_code)
        return pbp
    except APIError as e:
        print(f"Error getting play-by-play: {e}")
        return None


def display_game_summary(pbp: PlayByPlayResponse):
    """Display basic game summary from play-by-play data."""
    print(f"\n{'=' * 70}")
    print("GAME SUMMARY")
    print("=" * 70)

    print(f"\n{pbp.team_a} vs {pbp.team_b}")
    print(f"Total plays: {pbp.total_plays}")
    print(f"Live: {'Yes' if pbp.live else 'No'}")

    # Get final score from last play
    all_plays = pbp.all_plays
    if all_plays:
        last_play = all_plays[-1]
        if last_play.points_a is not None and last_play.points_b is not None:
            score_a, score_b = last_play.points_a, last_play.points_b
            print(f"Final Score: {pbp.team_a} {score_a} - {score_b} {pbp.team_b}")

    # Quarter breakdown
    print("\nPlays per quarter:")
    for q in range(1, 5):
        quarter_plays = pbp.get_quarter(q)
        print(f"  Q{q}: {len(quarter_plays)} plays")

    if pbp.extra_time:
        print(f"  OT: {len(pbp.extra_time)} plays")


def analyze_scoring_runs(pbp: PlayByPlayResponse, min_run: int = 6):
    """Analyze scoring runs in the game.

    A scoring run is a sequence of consecutive points by one team.
    """
    print(f"\n{'=' * 70}")
    print(f"SCORING RUNS (minimum {min_run} points)")
    print("=" * 70)

    scoring_plays = pbp.get_scoring_plays()
    if not scoring_plays:
        print("No scoring plays found")
        return

    runs = []
    current_team = None
    current_run = 0
    run_start_score = (0, 0)

    for play in scoring_plays:
        team = play.team_code.strip()

        if team == current_team:
            current_run += play.points_scored
        else:
            if current_run >= min_run and current_team:
                runs.append(
                    {
                        "team": current_team,
                        "points": current_run,
                        "start_score": run_start_score,
                        "end_score": (play.points_a or 0, play.points_b or 0),
                    }
                )
            current_team = team
            current_run = play.points_scored
            run_start_score = (play.points_a or 0, play.points_b or 0)

    # Check last run
    if current_run >= min_run and current_team:
        last_play = scoring_plays[-1]
        runs.append(
            {
                "team": current_team,
                "points": current_run,
                "start_score": run_start_score,
                "end_score": (last_play.points_a or 0, last_play.points_b or 0),
            }
        )

    if runs:
        print(f"\nFound {len(runs)} scoring run(s):\n")
        for i, run in enumerate(runs, 1):
            print(f"  {i}. {run['team']}: {run['points']}-0 run")
    else:
        print(f"\nNo scoring runs of {min_run}+ points found")


def analyze_player_performance(pbp: PlayByPlayResponse, top_n: int = 5):
    """Analyze individual player performance from play-by-play data."""
    print(f"\n{'=' * 70}")
    print("PLAYER PERFORMANCE")
    print("=" * 70)

    player_stats = defaultdict(
        lambda: {
            "name": "",
            "team": "",
            "points": 0,
            "2pt_made": 0,
            "2pt_att": 0,
            "3pt_made": 0,
            "3pt_att": 0,
            "ft_made": 0,
            "ft_att": 0,
            "assists": 0,
            "turnovers": 0,
            "steals": 0,
            "rebounds": 0,
        }
    )

    for play in pbp.all_plays:
        if not play.player_id:
            continue

        pid = play.player_id
        if play.player:
            player_stats[pid]["name"] = play.player
        if play.team:
            player_stats[pid]["team"] = play.team

        pt = play.play_type
        if pt == "2FGM":
            player_stats[pid]["2pt_made"] += 1
            player_stats[pid]["2pt_att"] += 1
            player_stats[pid]["points"] += 2
        elif pt == "2FGA":
            player_stats[pid]["2pt_att"] += 1
        elif pt == "3FGM":
            player_stats[pid]["3pt_made"] += 1
            player_stats[pid]["3pt_att"] += 1
            player_stats[pid]["points"] += 3
        elif pt == "3FGA":
            player_stats[pid]["3pt_att"] += 1
        elif pt == "FTM":
            player_stats[pid]["ft_made"] += 1
            player_stats[pid]["ft_att"] += 1
            player_stats[pid]["points"] += 1
        elif pt == "FTA":
            player_stats[pid]["ft_att"] += 1
        elif pt == "AS":
            player_stats[pid]["assists"] += 1
        elif pt == "TO":
            player_stats[pid]["turnovers"] += 1
        elif pt == "ST":
            player_stats[pid]["steals"] += 1
        elif pt in ("D", "O"):
            player_stats[pid]["rebounds"] += 1

    # Sort by points
    sorted_players = sorted(player_stats.items(), key=lambda x: x[1]["points"], reverse=True)

    print(f"\nTop {top_n} Scorers:")
    print("-" * 70)
    print(f"{'Player':<25}{'Team':<15}{'PTS':>6}{'2PT':>10}{'3PT':>10}{'FT':>10}")
    print("-" * 70)

    for pid, stats in sorted_players[:top_n]:
        name = stats["name"][:23] if stats["name"] else pid[:23]
        team = stats["team"][:13] if stats["team"] else "-"

        twopt = f"{stats['2pt_made']}/{stats['2pt_att']}"
        threept = f"{stats['3pt_made']}/{stats['3pt_att']}"
        ft = f"{stats['ft_made']}/{stats['ft_att']}"

        print(f"{name:<25}{team:<15}{stats['points']:>6}{twopt:>10}{threept:>10}{ft:>10}")


def analyze_shot_distribution(pbp: PlayByPlayResponse):
    """Analyze shot distribution by type."""
    print(f"\n{'=' * 70}")
    print("SHOT DISTRIBUTION")
    print("=" * 70)

    team_shots = {
        pbp.code_team_a.strip(): {
            "2pt_made": 0,
            "2pt_att": 0,
            "3pt_made": 0,
            "3pt_att": 0,
            "ft_made": 0,
            "ft_att": 0,
        },
        pbp.code_team_b.strip(): {
            "2pt_made": 0,
            "2pt_att": 0,
            "3pt_made": 0,
            "3pt_att": 0,
            "ft_made": 0,
            "ft_att": 0,
        },
    }

    for play in pbp.all_plays:
        team = play.team_code.strip()
        if team not in team_shots:
            continue

        pt = play.play_type
        if pt == "2FGM":
            team_shots[team]["2pt_made"] += 1
            team_shots[team]["2pt_att"] += 1
        elif pt == "2FGA":
            team_shots[team]["2pt_att"] += 1
        elif pt == "3FGM":
            team_shots[team]["3pt_made"] += 1
            team_shots[team]["3pt_att"] += 1
        elif pt == "3FGA":
            team_shots[team]["3pt_att"] += 1
        elif pt == "FTM":
            team_shots[team]["ft_made"] += 1
            team_shots[team]["ft_att"] += 1
        elif pt == "FTA":
            team_shots[team]["ft_att"] += 1

    print(f"\n{'Team':<15}{'2PT':>12}{'2PT%':>8}{'3PT':>12}{'3PT%':>8}{'FT':>12}{'FT%':>8}")
    print("-" * 75)

    for team, shots in team_shots.items():
        twopt = f"{shots['2pt_made']}/{shots['2pt_att']}"
        twopt_pct = (shots["2pt_made"] / shots["2pt_att"] * 100) if shots["2pt_att"] > 0 else 0

        threept = f"{shots['3pt_made']}/{shots['3pt_att']}"
        threept_pct = (shots["3pt_made"] / shots["3pt_att"] * 100) if shots["3pt_att"] > 0 else 0

        ft = f"{shots['ft_made']}/{shots['ft_att']}"
        ft_pct = (shots["ft_made"] / shots["ft_att"] * 100) if shots["ft_att"] > 0 else 0

        print(
            f"{team:<15}{twopt:>12}{twopt_pct:>7.1f}%{threept:>12}{threept_pct:>7.1f}%{ft:>12}{ft_pct:>7.1f}%"
        )


def display_quarter_timeline(pbp: PlayByPlayResponse, quarter: int):
    """Display timeline of plays for a specific quarter."""
    print(f"\n{'=' * 70}")
    print(f"QUARTER {quarter} TIMELINE")
    print("=" * 70)

    plays = pbp.get_quarter(quarter)
    if not plays:
        print(f"No plays found for quarter {quarter}")
        return

    print(f"\n{'Time':<8}{'Team':<15}{'Player':<20}{'Action':<25}{'Score'}")
    print("-" * 80)

    for play in plays[:30]:  # Limit to 30 plays for readability
        time = play.marker_time
        team = (play.team or "-")[:13]
        player = (play.player or "-")[:18]
        action = play.play_info[:23] if play.play_info else play.play_type

        score = ""
        if play.points_a is not None and play.points_b is not None:
            score = f"{play.points_a}-{play.points_b}"

        print(f"{time:<8}{team:<15}{player:<20}{action:<25}{score}")

    if len(plays) > 30:
        print(f"\n... and {len(plays) - 30} more plays")


def main():
    """Main function demonstrating play-by-play analysis capabilities."""
    print("=" * 70)
    print("EUROLEAGUE PLAY-BY-PLAY ANALYSIS")
    print("=" * 70)

    with EuroleagueClient() as client:
        # Example: Analyze a specific game
        # Season code format: E2025 for Euroleague 2024-25 season
        season_code = "E2025"
        game_code = 241  # Example game code

        print(f"\nFetching play-by-play for game {game_code} (season {season_code})...")

        pbp = get_play_by_play(client, season_code, game_code)

        if pbp:
            # Display various analyses
            display_game_summary(pbp)
            analyze_shot_distribution(pbp)
            analyze_player_performance(pbp)
            analyze_scoring_runs(pbp, min_run=6)
            display_quarter_timeline(pbp, quarter=1)
        else:
            print("Could not retrieve play-by-play data")


if __name__ == "__main__":
    main()
