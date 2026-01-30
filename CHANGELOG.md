# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2024-01-30

#### Live API - Real-time Game Data
- **Play-by-Play API** (`client.live.play_by_play`)
  - `get()` / `get_async()` - Fetch detailed play-by-play data for any game
  - `get_raw()` / `get_raw_async()` - Get raw JSON response
  - `PlayByPlayResponse` model with quarter-by-quarter breakdown
  - `PlayEvent` model with properties: `is_scoring_play`, `points_scored`, `is_shot_attempt`
  - Filtering methods: `get_plays_by_team()`, `get_plays_by_player()`, `get_scoring_plays()`, `get_quarter()`

- **Shot Location API** (`client.live.shots`)
  - `get()` / `get_async()` - Fetch shot data with court coordinates
  - `get_raw()` / `get_raw_async()` - Get raw JSON response
  - `ShotsResponse` model with shooting analysis methods
  - `Shot` model with coordinates (`coord_x`, `coord_y`), zones, and situational data
  - Properties: `is_made`, `is_three_pointer`, `is_two_pointer`, `is_free_throw`, `has_coordinates`
  - Filtering: `get_shots_by_team()`, `get_shots_by_player()`, `get_shots_by_zone()`
  - Statistics: `get_field_goal_percentage()`, `get_three_point_percentage()`, `get_free_throw_percentage()`
  - Situational analysis: fastbreak, second chance, points off turnover

#### New Examples
- `play_by_play_analysis.py` - Demonstrates play-by-play data analysis, scoring runs, player performance tracking
- `shot_chart_analysis.py` - Demonstrates shot location analysis, zone breakdowns, team comparisons

#### Development Tooling
- Pre-commit hooks configuration with ruff linting/formatting and mypy type checking
- CODEOWNERS file for repository governance

### Changed
- Updated CI workflow to test on latest Python versions
- Updated README with Live API documentation and examples
- Improved code formatting across examples
- Added `poetry.lock` for reproducible builds

### Fixed
- Type checking issues in Live API namespace imports

## [0.1.0] - 2024-01-28

### Added

- Initial release
- V1 API endpoints: games, players, results, schedules, standings, teams
- V2 API endpoints: clubs, competitions, games, groups, people, phases, records, referees, rounds, season_clubs, season_people, seasons, standings, stats
- V3 API endpoints: clubs, coaches, games, player_stats, team_stats, standings, stats
- Synchronous and asynchronous HTTP clients
- Automatic retry with exponential backoff
- Comprehensive exception handling
- Full type hints throughout

[unreleased]: https://github.com/sfendourakis/py-euroleague/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sfendourakis/py-euroleague/releases/tag/v0.1.0
