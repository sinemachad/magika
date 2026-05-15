"""Scoring utilities for Magika content type detection results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from magika.content_types import ContentType


@dataclass
class ScoredContentType:
    """A content type paired with a confidence score."""

    content_type: ContentType
    score: float

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(
                f"Score must be between 0.0 and 1.0, got {self.score}"
            )

    def __repr__(self) -> str:
        return (
            f"ScoredContentType(label={self.content_type.label!r}, "
            f"score={self.score:.4f})"
        )

    @property
    def is_high_confidence(self) -> bool:
        """Return True if score meets the high-confidence threshold."""
        return self.score >= 0.9


@dataclass
class ScoringResult:
    """Aggregated scoring result holding a ranked list of candidates."""

    candidates: List[ScoredContentType] = field(default_factory=list)

    def top(self) -> Optional[ScoredContentType]:
        """Return the highest-scored candidate, or None if empty."""
        if not self.candidates:
            return None
        return max(self.candidates, key=lambda c: c.score)

    def sorted_candidates(self) -> List[ScoredContentType]:
        """Return candidates sorted by score descending."""
        return sorted(self.candidates, key=lambda c: c.score, reverse=True)

    def filter_by_min_score(self, min_score: float) -> "ScoringResult":
        """Return a new ScoringResult containing only candidates above min_score."""
        filtered = [c for c in self.candidates if c.score >= min_score]
        return ScoringResult(candidates=filtered)

    def __len__(self) -> int:
        return len(self.candidates)
