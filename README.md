# py-euroleague

A Python wrapper for the Euroleague Basketball API. Access game statistics, player performance, team analytics, standings, and more.

## Installation

```bash
pip install py-euroleague
```

## Quick Start

```python
from euroleague import EuroleagueClient

client = EuroleagueClient()

# Get current season standings
standings = client.v3.standings.basic("E", "E2025", round_number=20)

# Get top scorers
leaders = client.v3.player_stats.leaders("E", season_code="E2025", limit=10)
for player in leaders["points"][:5]:
    name = player["details"]["name"]
    ppg = player["average"]
    print(f"{name}: {ppg:.1f} PPG")

client.close()
```

Or use as a context manager:

```python
with EuroleagueClient() as client:
    clubs = client.v2.clubs.list(limit=10)
    print(f"Found {len(clubs['data'])} clubs")
```

## Statistics & Analytics

### Player Statistics

```python
with EuroleagueClient() as client:
    # Season leaders across all categories
    leaders = client.v3.player_stats.leaders(
        competition_code="E",
        season_code="E2025",
        limit=20
    )

    # Access different stat categories
    top_scorers = leaders["points"]
    top_rebounders = leaders["rebounds"]
    top_playmakers = leaders["assists"]
    top_pir = leaders["pir"]  # Performance Index Rating

    # Traditional stats (per-game averages)
    traditional = client.v3.player_stats.traditional(
        competition_code="E",
        season_code="E2025"
    )

    # Advanced analytics
    advanced = client.v3.player_stats.advanced(
        competition_code="E",
        season_code="E2025"
    )
```

### Team Statistics

```python
with EuroleagueClient() as client:
    # Team traditional stats
    team_stats = client.v3.team_stats.traditional(
        competition_code="E",
        season_code="E2025"
    )

    for team in team_stats["teams"][:5]:
        name = team["team"]["name"]
        ppg = team["pointsScored"]
        print(f"{name}: {ppg:.1f} PPG")

    # Team advanced stats
    advanced = client.v3.team_stats.advanced(
        competition_code="E",
        season_code="E2025"
    )

    # Opponent stats (defensive analysis)
    opponent_stats = client.v3.team_stats.opponents(
        competition_code="E",
        season_code="E2025"
    )
```

### Game Box Scores

```python
with EuroleagueClient() as client:
    # Get game stats with full box score
    game_stats = client.v3.stats.get_game_stats("E", "E2025", game_code=100)

    # Home team stats
    home = game_stats["local"]
    home_total = home["total"]
    print(f"Home: {home_total['points']} points")

    # Individual player stats
    for player in home["players"]:
        name = player["player"]["person"]["name"]
        pts = player["stats"]["points"]
        reb = player["stats"]["totalRebounds"]
        ast = player["stats"]["assistances"]
        print(f"  {name}: {pts} PTS, {reb} REB, {ast} AST")
```

## Live Game Data

Access real-time game data including play-by-play events and shot locations with coordinates.

### Play-by-Play

Get detailed play-by-play data for any game:

```python
with EuroleagueClient() as client:
    # Get play-by-play for a game
    pbp = client.live.play_by_play.get("E2025", game_code=241)

    print(f"{pbp.team_a} vs {pbp.team_b}")
    print(f"Total plays: {pbp.total_plays}")

    # Get plays by quarter
    for q in range(1, 5):
        quarter_plays = pbp.get_quarter(q)
        print(f"Q{q}: {len(quarter_plays)} plays")

    # Filter scoring plays
    for play in pbp.get_scoring_plays()[:10]:
        print(f"{play.marker_time} - {play.player}: {play.play_info} ({play.points_scored} pts)")

    # Get plays by team or player
    team_plays = pbp.get_plays_by_team("MAD")
    player_plays = pbp.get_plays_by_player("P001")
```

### Shot Location Data

Get shot data with court coordinates for shot chart analysis:

```python
with EuroleagueClient() as client:
    # Get shot data for a game
    shots = client.live.shots.get("E2025", game_code=241)

    print(f"Total shots: {shots.total_shots}")
    print(f"FG%: {shots.get_field_goal_percentage():.1f}%")
    print(f"3PT%: {shots.get_three_point_percentage():.1f}%")

    # Get shots with coordinates for visualization
    for shot in shots.field_goals:
        if shot.has_coordinates:
            status = "Made" if shot.is_made else "Missed"
            print(f"{shot.player}: {status} at ({shot.coord_x}, {shot.coord_y})")

    # Filter by team, player, or zone
    team_shots = shots.get_shots_by_team("MAD")
    player_shots = shots.get_shots_by_player("P001")
    paint_shots = shots.get_shots_by_zone("C")

    # Analyze special situations
    fastbreak_shots = [s for s in shots.field_goals if s.fastbreak]
    second_chance = [s for s in shots.field_goals if s.second_chance]
```

### Standings & Rankings

```python
with EuroleagueClient() as client:
    # Current standings
    standings = client.v3.standings.basic("E", "E2025", round_number=20)

    # Streak analysis
    streaks = client.v3.standings.streaks("E", "E2025", round_number=20)

    # Point differential margins
    margins = client.v3.standings.margins("E", "E2025", round_number=20)
```

## Async Support

For better performance with multiple requests:

```python
import asyncio
from euroleague import AsyncEuroleagueClient

async def analyze_season():
    async with AsyncEuroleagueClient() as client:
        # Parallel requests
        leaders, team_stats, standings = await asyncio.gather(
            client.v3.player_stats.leaders_async("E", season_code="E2025"),
            client.v3.team_stats.traditional_async("E", season_code="E2025"),
            client.v3.standings.basic_async("E", "E2025", 20)
        )
        return leaders, team_stats, standings

asyncio.run(analyze_season())
```

## API Versions

The Euroleague API has multiple versions and endpoints:

| Version | Focus | Best For |
|---------|-------|----------|
| **V1** | Legacy/Simple | Basic box scores, standings |
| **V2** | Comprehensive | Clubs, games, people, seasons |
| **V3** | Statistics | Player/team stats, analytics |
| **Live** | Real-time | Play-by-play, shot locations |

### V1 Endpoints
- `client.v1.standings` - League standings
- `client.v1.games` - Box scores
- `client.v1.players` - Player stats
- `client.v1.teams` - Team rosters

### V2 Endpoints
- `client.v2.clubs` - Club information
- `client.v2.games` - Game details and history
- `client.v2.people` - Players, coaches, personnel
- `client.v2.seasons` - Season information
- `client.v2.standings` - Detailed standings

### V3 Endpoints (Recommended for Analytics)
- `client.v3.player_stats` - Leaders, traditional, advanced, scoring stats
- `client.v3.team_stats` - Traditional, advanced, opponent stats
- `client.v3.standings` - Basic, streaks, margins, calendar views
- `client.v3.stats` - Game stats, team comparisons

### Live Endpoints (Real-time Game Data)
- `client.live.play_by_play` - Play-by-play events with timestamps
- `client.live.shots` - Shot locations with court coordinates

## Competition Codes

- `E` - EuroLeague
- `U` - EuroCup

## Examples

See the [examples/](examples/) directory for complete working examples:

- **basic_usage.py** - Getting started with the API
- **player_analysis.py** - Player statistics and comparisons
- **team_analysis.py** - Team performance analysis
- **game_analysis.py** - Game results and box scores
- **player_game_logs.py** - Game-by-game player statistics
- **fantasy_basketball.py** - Fantasy basketball analysis
- **async_example.py** - Async client usage
- **play_by_play_analysis.py** - Play-by-play data analysis
- **shot_chart_analysis.py** - Shot location data with coordinates

## Error Handling

```python
from euroleague import EuroleagueClient
from euroleague.exceptions import NotFoundError, RateLimitError, APIError

with EuroleagueClient() as client:
    try:
        player = client.v2.people.get("INVALID_CODE")
    except NotFoundError:
        print("Player not found")
    except RateLimitError as e:
        print(f"Rate limited. Retry after {e.retry_after}s")
    except APIError as e:
        print(f"API error: {e.message}")
```

## License

MIT License - see LICENSE file for details.

## Links

- [Euroleague API Documentation](https://api-live.euroleague.net/swagger/index.html)
