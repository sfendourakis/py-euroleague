"""Async usage example for py-euroleague."""

import asyncio

from euroleague import AsyncEuroleagueClient
from euroleague.exceptions import APIError, NotFoundError


async def main():
    """Main async example demonstrating parallel API calls."""
    print("\n--- Parallel API Calls ---")
    async with AsyncEuroleagueClient() as client:
        # Parallel API calls for better performance
        clubs, competitions = await asyncio.gather(
            client.v2.clubs.list_async(limit=5),
            client.v2.competitions.list_async(),
        )

        print(f"Fetched {len(clubs.get('data', []))} clubs")
        print(f"Fetched {len(competitions.get('data', []))} competitions")


async def example_sequential():
    """Sequential async calls example."""
    print("\n--- Sequential API Calls ---")
    async with AsyncEuroleagueClient() as client:
        # Get clubs first
        clubs = await client.v2.clubs.list_async(limit=5)
        print(f"Found {len(clubs.get('data', []))} clubs")

        # Then get details for a specific club
        for club_data in clubs.get("data", [])[:2]:
            club_code = club_data.get("code")
            if club_code:
                try:
                    info = await client.v2.clubs.get_async(club_code)
                    print(f"  Club {club_code}: {info.get('name', 'N/A')}")
                except NotFoundError:
                    print(f"  Club {club_code}: Not found")


async def example_error_handling():
    """Error handling example."""
    print("\n--- Error Handling ---")
    async with AsyncEuroleagueClient() as client:
        try:
            clubs = await client.v2.clubs.list_async(limit=3)
            print(f"Successfully fetched {len(clubs.get('data', []))} clubs")
        except NotFoundError as e:
            print(f"Resource not found: {e}")
        except APIError as e:
            print(f"API error [{e.status_code}]: {e.message}")


if __name__ == "__main__":
    print("py-euroleague Async Usage Examples")
    print("=" * 40)

    asyncio.run(main())
    asyncio.run(example_sequential())
    asyncio.run(example_error_handling())

    print("\nDone!")
