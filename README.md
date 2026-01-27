# py-euroleague

A Python wrapper for the Euroleague Basketball API, providing easy access to game statistics, standings, player information, and more.

## Features

- **Full API Coverage**: Supports all three API versions (v1, v2, v3)
- **Type Hints**: Full type annotations for IDE support
- **Sync & Async**: Both synchronous and asynchronous clients
- **OAuth2 PKCE**: Secure authentication flow
- **Automatic Retries**: Built-in retry logic for failed requests
- **Token Persistence**: File-based token storage for session persistence

## Installation

```bash
pip install py-euroleague
```

For development:
```bash
pip install py-euroleague[dev]
```

## Quick Start

### Authentication

The Euroleague API requires OAuth2 PKCE authentication:

```python
from euroleague import EuroleagueClient

client = EuroleagueClient(client_id="your_client_id")

# Step 1: Get authorization URL
auth_url, state, verifier = client.get_authorization_url()
print(f"Visit: {auth_url}")

# Step 2: After user authorizes, exchange the code
client.authenticate(code="code_from_redirect", code_verifier=verifier)
```

Or use a pre-obtained token:

```python
from euroleague import EuroleagueClient
from euroleague.auth import TokenInfo

client = EuroleagueClient(client_id="your_client_id")
client.set_token(TokenInfo(
    access_token="your_access_token",
    token_type="Bearer",
    expires_in=3600
))
```

### Basic Usage

```python
from euroleague import EuroleagueClient

with EuroleagueClient(client_id="your_client_id") as client:
    # V1 API - Simple/Legacy endpoints
    standings = client.v1.standings.get(season_code="E2024")
    box_score = client.v1.games.get(season_code="E2024", game_code=1)

    # V2 API - Comprehensive endpoints
    clubs = client.v2.clubs.list()
    games = client.v2.games.list(competition_code="E", season_code="2024")
    players = client.v2.season_people.list(
        competition_code="E",
        season_code="2024",
        person_type="Player"
    )

    # V3 API - Statistics-focused endpoints
    leaders = client.v3.player_stats.leaders(competition_code="E")
    advanced = client.v3.player_stats.advanced(
        competition_code="E",
        season_code="2024"
    )
    team_stats = client.v3.team_stats.traditional(competition_code="E")
```

### Async Usage

```python
import asyncio
from euroleague import AsyncEuroleagueClient

async def main():
    async with AsyncEuroleagueClient(client_id="your_client_id") as client:
        # Parallel requests for better performance
        games, standings, leaders = await asyncio.gather(
            client.v2.games.list_async("E", "2024"),
            client.v3.standings.basic_async("E", "2024", 10),
            client.v3.player_stats.leaders_async("E")
        )
        print(f"Found {len(games['data'])} games")

asyncio.run(main())
```

## API Structure

### V1 API (Legacy/Simple)
- `client.v1.games` - Box scores
- `client.v1.players` - Player stats
- `client.v1.results` - Game results
- `client.v1.schedules` - Schedules
- `client.v1.standings` - Standings
- `client.v1.teams` - Teams with rosters

### V2 API (Comprehensive)
- `client.v2.clubs` - Club information
- `client.v2.competitions` - Competition data
- `client.v2.games` - Game details and history
- `client.v2.groups` - Phase groups
- `client.v2.people` - Players, coaches, personnel
- `client.v2.phases` - Season phases
- `client.v2.records` - Historical records
- `client.v2.referees` - Referee information
- `client.v2.rounds` - Round information
- `client.v2.season_clubs` - Season-specific club data
- `client.v2.season_people` - Season-specific personnel
- `client.v2.seasons` - Season information
- `client.v2.standings` - Detailed standings
- `client.v2.stats` - Club statistics

### V3 API (Statistics-focused)
- `client.v3.clubs` - Club info
- `client.v3.coaches` - Coach records
- `client.v3.games` - Match reports
- `client.v3.player_stats` - Player statistics (leaders, traditional, advanced, misc, scoring)
- `client.v3.team_stats` - Team statistics (leaders, traditional, advanced, opponents)
- `client.v3.standings` - Various standings views (basic, calendar, streaks, margins, ahead/behind)
- `client.v3.stats` - Game and comparison stats

## Competition Codes

- `E` - EuroLeague
- `U` - EuroCup

## Error Handling

```python
from euroleague import EuroleagueClient
from euroleague.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    APIError
)

client = EuroleagueClient(client_id="your_client_id")

try:
    player = client.v2.people.get("INVALID_CODE")
except NotFoundError as e:
    print(f"Not found: {e.identifier}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except AuthenticationError:
    print("Please authenticate")
except APIError as e:
    print(f"API error [{e.status_code}]: {e.message}")
```

## Custom Token Storage

For distributed applications or custom persistence:

```python
from euroleague import EuroleagueClient
from euroleague.auth import TokenStorage, TokenInfo

class RedisTokenStorage(TokenStorage):
    def __init__(self, redis_client, key="euroleague:token"):
        self.redis = redis_client
        self.key = key

    def store_token(self, token: TokenInfo) -> None:
        self.redis.set(self.key, token.to_dict())

    def get_token(self) -> TokenInfo | None:
        data = self.redis.get(self.key)
        return TokenInfo.from_dict(data) if data else None

    def clear_token(self) -> None:
        self.redis.delete(self.key)

# Use custom storage
storage = RedisTokenStorage(redis_client)
client = EuroleagueClient(client_id="...", token_storage=storage)
```

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/py-euroleague.git
cd py-euroleague

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/euroleague

# Linting
ruff check src/
```

## License

MIT License - see LICENSE file for details.

## Links

- [Euroleague API Documentation](https://api-live.euroleague.net/swagger/index.html)
- [GitHub Repository](https://github.com/yourusername/py-euroleague)
