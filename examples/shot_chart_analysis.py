"""
Shot Chart Analysis Example

This example demonstrates how to:
- Fetch shot location data with coordinates for a game
- Analyze shooting by court zones
- Calculate shooting percentages by shot type
- Identify hot and cold zones
- Compare team shooting efficiency
"""

from collections import defaultdict

from euroleague import EuroleagueClient
from euroleague.exceptions import APIError
from euroleague.models.live.shots import ShotsResponse


def get_shots(client: EuroleagueClient, season_code: str, game_code: int) -> ShotsResponse | None:
    """Get shot data for a game."""
    try:
        shots = client.live.shots.get(season_code, game_code)
        return shots
    except APIError as e:
        print(f"Error getting shot data: {e}")
        return None


def display_game_summary(shots: ShotsResponse):
    """Display basic shooting summary for the game."""
    print(f"\n{'=' * 70}")
    print("SHOOTING SUMMARY")
    print("=" * 70)

    print(f"\nTotal shots: {shots.total_shots}")
    print(f"Field goals: {len(shots.field_goals)}")
    print(f"Free throws: {len(shots.free_throws)}")

    fg_pct = shots.get_field_goal_percentage()
    print(f"\nOverall FG%: {fg_pct:.1f}%")

    three_pct = shots.get_three_point_percentage()
    if shots.three_pointers:
        made_3 = sum(1 for s in shots.three_pointers if s.is_made)
        print(f"3PT: {made_3}/{len(shots.three_pointers)} ({three_pct:.1f}%)")

    two_pct = shots.get_shooting_percentage(shots.two_pointers)
    if shots.two_pointers:
        made_2 = sum(1 for s in shots.two_pointers if s.is_made)
        print(f"2PT: {made_2}/{len(shots.two_pointers)} ({two_pct:.1f}%)")

    ft_pct = shots.get_free_throw_percentage()
    if shots.free_throws:
        made_ft = sum(1 for s in shots.free_throws if s.is_made)
        print(f"FT: {made_ft}/{len(shots.free_throws)} ({ft_pct:.1f}%)")


def analyze_by_zone(shots: ShotsResponse):
    """Analyze shooting efficiency by court zone."""
    print(f"\n{'=' * 70}")
    print("SHOOTING BY ZONE")
    print("=" * 70)

    # Court zones are typically labeled A-I
    zone_stats = defaultdict(lambda: {"made": 0, "attempted": 0})

    for shot in shots.field_goals:
        if shot.zone:
            zone_stats[shot.zone]["attempted"] += 1
            if shot.is_made:
                zone_stats[shot.zone]["made"] += 1

    if not zone_stats:
        print("\nNo zone data available")
        return

    print(f"\n{'Zone':<8}{'Made':<8}{'Att':<8}{'FG%':>8}")
    print("-" * 32)

    for zone in sorted(zone_stats.keys()):
        stats = zone_stats[zone]
        pct = (stats["made"] / stats["attempted"] * 100) if stats["attempted"] > 0 else 0
        print(f"{zone:<8}{stats['made']:<8}{stats['attempted']:<8}{pct:>7.1f}%")


def analyze_team_comparison(shots: ShotsResponse):
    """Compare shooting between the two teams."""
    print(f"\n{'=' * 70}")
    print("TEAM SHOOTING COMPARISON")
    print("=" * 70)

    # Get unique team codes
    teams = set()
    for shot in shots.all_shots:
        teams.add(shot.team_code)

    if len(teams) < 2:
        print("\nCould not identify both teams")
        return

    team_list = sorted(teams)

    print(f"\n{'Stat':<20}", end="")
    for team in team_list:
        print(f"{team:>15}", end="")
    print()
    print("-" * 50)

    # Field Goals
    print(f"{'Field Goals':<20}", end="")
    for team in team_list:
        team_shots = shots.get_shots_by_team(team)
        fg = [s for s in team_shots if not s.is_free_throw]
        made = sum(1 for s in fg if s.is_made)
        print(f"{made}/{len(fg):>15}", end="")
    print()

    # FG%
    print(f"{'FG%':<20}", end="")
    for team in team_list:
        team_shots = shots.get_shots_by_team(team)
        fg = [s for s in team_shots if not s.is_free_throw]
        if fg:
            pct = sum(1 for s in fg if s.is_made) / len(fg) * 100
            print(f"{pct:>14.1f}%", end="")
        else:
            print(f"{'N/A':>15}", end="")
    print()

    # 3-pointers
    print(f"{'3PT':<20}", end="")
    for team in team_list:
        team_shots = shots.get_shots_by_team(team)
        threes = [s for s in team_shots if s.is_three_pointer]
        made = sum(1 for s in threes if s.is_made)
        print(f"{made}/{len(threes):>15}", end="")
    print()

    # 3PT%
    print(f"{'3PT%':<20}", end="")
    for team in team_list:
        team_shots = shots.get_shots_by_team(team)
        threes = [s for s in team_shots if s.is_three_pointer]
        if threes:
            pct = sum(1 for s in threes if s.is_made) / len(threes) * 100
            print(f"{pct:>14.1f}%", end="")
        else:
            print(f"{'N/A':>15}", end="")
    print()

    # 2-pointers
    print(f"{'2PT':<20}", end="")
    for team in team_list:
        team_shots = shots.get_shots_by_team(team)
        twos = [s for s in team_shots if s.is_two_pointer]
        made = sum(1 for s in twos if s.is_made)
        print(f"{made}/{len(twos):>15}", end="")
    print()

    # 2PT%
    print(f"{'2PT%':<20}", end="")
    for team in team_list:
        team_shots = shots.get_shots_by_team(team)
        twos = [s for s in team_shots if s.is_two_pointer]
        if twos:
            pct = sum(1 for s in twos if s.is_made) / len(twos) * 100
            print(f"{pct:>14.1f}%", end="")
        else:
            print(f"{'N/A':>15}", end="")
    print()

    # Free throws
    print(f"{'FT':<20}", end="")
    for team in team_list:
        team_shots = shots.get_shots_by_team(team)
        ft = [s for s in team_shots if s.is_free_throw]
        made = sum(1 for s in ft if s.is_made)
        print(f"{made}/{len(ft):>15}", end="")
    print()


def analyze_special_situations(shots: ShotsResponse):
    """Analyze shots in special situations (fastbreak, second chance, etc.)."""
    print(f"\n{'=' * 70}")
    print("SPECIAL SITUATIONS")
    print("=" * 70)

    fg = shots.field_goals

    # Fastbreak
    fastbreak = [s for s in fg if s.fastbreak]
    if fastbreak:
        fb_made = sum(1 for s in fastbreak if s.is_made)
        fb_pct = fb_made / len(fastbreak) * 100
        print(f"\nFastbreak: {fb_made}/{len(fastbreak)} ({fb_pct:.1f}%)")

    # Second chance
    second_chance = [s for s in fg if s.second_chance]
    if second_chance:
        sc_made = sum(1 for s in second_chance if s.is_made)
        sc_pct = sc_made / len(second_chance) * 100
        print(f"Second Chance: {sc_made}/{len(second_chance)} ({sc_pct:.1f}%)")

    # Points off turnovers
    pot = [s for s in fg if s.points_off_turnover]
    if pot:
        pot_made = sum(1 for s in pot if s.is_made)
        pot_pct = pot_made / len(pot) * 100
        print(f"Points off TO: {pot_made}/{len(pot)} ({pot_pct:.1f}%)")


def display_top_shooters(shots: ShotsResponse, top_n: int = 5):
    """Display top shooters by field goals made."""
    print(f"\n{'=' * 70}")
    print("TOP SHOOTERS")
    print("=" * 70)

    player_stats = defaultdict(
        lambda: {"name": "", "team": "", "fg_made": 0, "fg_att": 0, "pts": 0}
    )

    for shot in shots.field_goals:
        pid = shot.player_id
        player_stats[pid]["name"] = shot.player
        player_stats[pid]["team"] = shot.team_code
        player_stats[pid]["fg_att"] += 1
        player_stats[pid]["pts"] += shot.points if shot.is_made else 0
        if shot.is_made:
            player_stats[pid]["fg_made"] += 1

    # Sort by field goals made
    sorted_players = sorted(player_stats.items(), key=lambda x: x[1]["fg_made"], reverse=True)

    print(f"\n{'Player':<25}{'Team':<8}{'FGM':<6}{'FGA':<6}{'FG%':>8}{'PTS':>6}")
    print("-" * 60)

    for pid, stats in sorted_players[:top_n]:
        name = stats["name"][:23] if stats["name"] else pid[:23]
        team = stats["team"][:6]
        pct = stats["fg_made"] / stats["fg_att"] * 100 if stats["fg_att"] > 0 else 0
        print(
            f"{name:<25}{team:<8}{stats['fg_made']:<6}{stats['fg_att']:<6}"
            f"{pct:>7.1f}%{stats['pts']:>6}"
        )


def display_shot_coordinates(shots: ShotsResponse, limit: int = 20):
    """Display shot coordinates for visualization."""
    print(f"\n{'=' * 70}")
    print("SHOT COORDINATES (for shot chart)")
    print("=" * 70)

    fg_with_coords = [s for s in shots.field_goals if s.has_coordinates]

    if not fg_with_coords:
        print("\nNo coordinate data available")
        return

    print(f"\nShowing first {limit} shots with coordinates:")
    print(f"\n{'Player':<20}{'Result':<8}{'X':>8}{'Y':>8}{'Zone':>6}")
    print("-" * 52)

    for shot in fg_with_coords[:limit]:
        name = shot.player[:18] if shot.player else "Unknown"
        result = "Made" if shot.is_made else "Missed"
        print(f"{name:<20}{result:<8}{shot.coord_x:>8}{shot.coord_y:>8}{shot.zone:>6}")

    total = len(fg_with_coords)
    if total > limit:
        print(f"\n... and {total - limit} more shots with coordinates")

    print(f"\nTotal shots with coordinates: {total}")
    print("Coordinate system: X and Y represent court position")
    print("(-1, -1) indicates free throws (no court position)")


def main():
    """Main function demonstrating shot chart analysis capabilities."""
    print("=" * 70)
    print("EUROLEAGUE SHOT CHART ANALYSIS")
    print("=" * 70)

    with EuroleagueClient() as client:
        # Example: Analyze a specific game
        # Season code format: E2025 for Euroleague 2024-25 season
        season_code = "E2025"
        game_code = 241  # Example game code

        print(f"\nFetching shot data for game {game_code} (season {season_code})...")

        shots = get_shots(client, season_code, game_code)

        if shots:
            display_game_summary(shots)
            analyze_team_comparison(shots)
            analyze_by_zone(shots)
            analyze_special_situations(shots)
            display_top_shooters(shots)
            display_shot_coordinates(shots)
        else:
            print("Could not retrieve shot data")


if __name__ == "__main__":
    main()
