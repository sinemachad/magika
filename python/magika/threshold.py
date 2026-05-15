"""Threshold configuration for Magika detection confidence levels."""

from __future__ import annotations

from dataclasses import dataclass


# Default thresholds used across the detection pipeline
DEFAULT_HIGH_CONFIDENCE_THRESHOLD: float = 0.9
DEFAULT_MEDIUM_CONFIDENCE_THRESHOLD: float = 0.7
DEFAULT_LOW_CONFIDENCE_THRESHOLD: float = 0.5


@dataclass(frozen=True)
class ThresholdConfig:
    """Immutable configuration for confidence thresholds."""

    high: float = DEFAULT_HIGH_CONFIDENCE_THRESHOLD
    medium: float = DEFAULT_MEDIUM_CONFIDENCE_THRESHOLD
    low: float = DEFAULT_LOW_CONFIDENCE_THRESHOLD

    def __post_init__(self) -> None:
        for name, value in [("high", self.high), ("medium", self.medium), ("low", self.low)]:
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"Threshold '{name}' must be between 0.0 and 1.0, got {value}"
                )
        if not (self.low <= self.medium <= self.high):
            raise ValueError(
                "Thresholds must satisfy: low <= medium <= high, "
                f"got low={self.low}, medium={self.medium}, high={self.high}"
            )

    def classify_score(self, score: float) -> str:
        """Classify a score as 'high', 'medium', 'low', or 'unknown'."""
        if score >= self.high:
            return "high"
        if score >= self.medium:
            return "medium"
        if score >= self.low:
            return "low"
        return "unknown"


DEFAULT_THRESHOLD_CONFIG = ThresholdConfig()
