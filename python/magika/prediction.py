"""Prediction result types for Magika."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from magika.content_types import ContentType
from magika.scorer import ScoringResult


@dataclass(frozen=True)
class PredictionMode:
    """Constants for prediction modes."""

    HIGH_CONFIDENCE: str = "high_confidence"
    BEST_GUESS: str = "best_guess"
    MAGIC_BYTES: str = "magic_bytes"


@dataclass
class PredictionResult:
    """Encapsulates the full result of a Magika prediction for a single file."""

    path: Optional[Path]
    dl: ScoringResult
    output: ContentType
    mode: str

    def __post_init__(self) -> None:
        if self.path is not None and not isinstance(self.path, Path):
            raise TypeError(f"path must be a Path or None, got {type(self.path)}")
        if not isinstance(self.dl, ScoringResult):
            raise TypeError(f"dl must be a ScoringResult, got {type(self.dl)}")
        if not isinstance(self.output, ContentType):
            raise TypeError(f"output must be a ContentType, got {type(self.output)}")
        valid_modes = {
            PredictionMode.HIGH_CONFIDENCE,
            PredictionMode.BEST_GUESS,
            PredictionMode.MAGIC_BYTES,
        }
        if self.mode not in valid_modes:
            raise ValueError(f"mode must be one of {valid_modes}, got {self.mode!r}")

    @property
    def is_high_confidence(self) -> bool:
        """Return True if the prediction was made with high confidence."""
        return self.mode == PredictionMode.HIGH_CONFIDENCE

    @property
    def label(self) -> str:
        """Convenience accessor for the output content type label."""
        return str(self.output)

    def __repr__(self) -> str:
        path_str = str(self.path) if self.path is not None else "<bytes>"
        return (
            f"PredictionResult(path={path_str!r}, label={self.label!r}, "
            f"score={self.dl.score:.4f}, mode={self.mode!r})"
        )
