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

The Euroleague API has three versions, each with different focuses:

| Version | Focus | Best For |
|---------|-------|----------|
| **V1** | Legacy/Simple | Basic box scores, standings |
| **V2** | Comprehensive | Clubs, games, people, seasons |
| **V3** | Statistics | Player/team stats, analytics |

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
