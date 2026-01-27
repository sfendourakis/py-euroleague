"""Async usage example for py-euroleague."""

import asyncio

from euroleague import AsyncEuroleagueClient
from euroleague.auth import TokenInfo


async def main():
    """Main async example."""
    # Initialize the async client
    async with AsyncEuroleagueClient(client_id="your_client_id") as client:
        # Set a pre-obtained token (or use OAuth2 flow)
        # client.set_token(TokenInfo(
        #     access_token="your_access_token",
        #     token_type="Bearer",
        #     expires_in=3600
        # ))

        # Example: Parallel API calls for better performance
        # This fetches all data simultaneously instead of sequentially
        games, standings, player_leaders, team_stats = await asyncio.gather(
            client.v2.games.list_async(
                competition_code="E",
                season_code="2024",
                limit=10
            ),
            client.v3.standings.basic_async("E", "2024", 10),
            client.v3.player_stats.leaders_async("E", season_code="2024"),
            client.v3.team_stats.traditional_async("E", season_code="2024"),
        )

        print(f"Fetched {len(games.get('data', []))} games")
        print(f"Standings: {standings}")
        print(f"Player Leaders: {player_leaders}")
        print(f"Team Stats: {team_stats}")


async def example_sequential():
    """Sequential async calls example."""
    async with AsyncEuroleagueClient(client_id="your_client_id") as client:
        # Get clubs first
        clubs = await client.v2.clubs.list_async(limit=5)
        print("Clubs:", clubs)

        # Then get details for each club (could be parallelized)
        for club_data in clubs.get("data", [])[:3]:
            club_code = club_data.get("clubCode")
            if club_code:
                info = await client.v2.clubs.get_info_async(club_code)
                print(f"Club {club_code} info:", info)


async def example_error_handling():
    """Error handling example."""
    from euroleague.exceptions import (
        AuthenticationError,
        NotFoundError,
        RateLimitError,
        APIError,
    )

    async with AsyncEuroleagueClient(client_id="your_client_id") as client:
        try:
            # This will likely fail without proper authentication
            clubs = await client.v2.clubs.list_async()
            print("Clubs:", clubs)
        except AuthenticationError as e:
            print(f"Authentication failed: {e}")
            print("Please set a valid token or complete OAuth2 flow")
        except NotFoundError as e:
            print(f"Resource not found: {e.resource_type} - {e.identifier}")
        except RateLimitError as e:
            print(f"Rate limited! Retry after {e.retry_after} seconds")
            await asyncio.sleep(e.retry_after or 60)
        except APIError as e:
            print(f"API error [{e.status_code}]: {e.message}")


if __name__ == "__main__":
    print("py-euroleague Async Usage Examples")
    print("=" * 40)
    print("\nNote: You need to authenticate before making API calls.")

    # Run the main example
    # asyncio.run(main())

    # Or run sequential example
    # asyncio.run(example_sequential())

    # Or run error handling example
    # asyncio.run(example_error_handling())
