"""Base model classes for Euroleague API responses."""

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class EuroleagueModel(BaseModel):
    """Base model with common configuration for all Euroleague API responses."""

    model_config = ConfigDict(
        populate_by_name=True,  # Allow field population by alias
        str_strip_whitespace=True,
        frozen=False,
        extra="ignore",  # Ignore unknown fields from API
    )


class PaginatedResponse(EuroleagueModel, Generic[T]):
    """Generic paginated response wrapper."""

    data: list[T]
    total: int
    offset: int = 0
    limit: int = 20

    @property
    def has_next(self) -> bool:
        """Check if there are more pages available."""
        return self.offset + self.limit < self.total

    @property
    def has_previous(self) -> bool:
        """Check if there is a previous page."""
        return self.offset > 0

    @property
    def page(self) -> int:
        """Current page number (1-indexed)."""
        if self.limit == 0:
            return 1
        return (self.offset // self.limit) + 1

    @property
    def total_pages(self) -> int:
        """Total number of pages."""
        if self.limit == 0:
            return 1
        return (self.total + self.limit - 1) // self.limit
