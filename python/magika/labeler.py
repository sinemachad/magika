"""Label assignment logic: maps raw model output to a final content-type label.

Given a ScoringResult this module decides which ContentType label to surface,
respecting the configured prediction mode and confidence thresholds.
"""

from __future__ import annotations

from dataclasses import dataclass

from magika.content_types import ContentType
from magika.prediction import PredictionMode, PredictionResult
from magika.scorer import ScoringResult
from magika.threshold import ThresholdConfig


@dataclass(frozen=True)
class LabelingConfig:
    """Runtime configuration that controls label-assignment behaviour."""

    mode: str = PredictionMode.HIGH_CONFIDENCE
    threshold: ThresholdConfig = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.threshold is None:
            object.__setattr__(self, "threshold", ThresholdConfig())
        if self.mode not in (
            PredictionMode.HIGH_CONFIDENCE,
            PredictionMode.MEDIUM_CONFIDENCE,
            PredictionMode.BEST_GUESS,
        ):
            raise ValueError(f"Unknown prediction mode: {self.mode!r}")


def assign_label(
    scoring: ScoringResult,
    fallback: ContentType,
    config: LabelingConfig | None = None,
) -> PredictionResult:
    """Return a :class:`PredictionResult` for *scoring*.

    Parameters
    ----------
    scoring:
        The ranked scoring result produced by the model.
    fallback:
        Content type to use when confidence is too low.
    config:
        Labeling configuration; defaults are used when *None*.
    """
    if config is None:
        config = LabelingConfig()

    top = scoring.top
    mode = config.mode
    threshold = config.threshold

    if mode == PredictionMode.BEST_GUESS:
        # Always trust the top prediction regardless of score.
        return PredictionResult(content_type=top.content_type, scoring=scoring, mode=mode)

    high_conf = threshold.classify_score(top.score) == "high"

    if mode == PredictionMode.HIGH_CONFIDENCE:
        ct = top.content_type if high_conf else fallback
    else:  # MEDIUM_CONFIDENCE
        medium_conf = top.score >= threshold.medium
        ct = top.content_type if medium_conf else fallback

    return PredictionResult(content_type=ct, scoring=scoring, mode=mode)
