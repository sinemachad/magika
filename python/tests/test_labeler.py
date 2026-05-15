"""Tests for magika.labeler — label assignment logic."""

from __future__ import annotations

import pytest

from magika.content_types import ContentType
from magika.labeler import LabelingConfig, assign_label
from magika.prediction import PredictionMode
from magika.scorer import ScoredContentType, ScoringResult
from magika.threshold import ThresholdConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ct(label: str) -> ContentType:
    return ContentType(
        label=label,
        mime_type=f"application/{label}",
        group="test",
        description=label,
        extensions=[],
        is_text=False,
    )


def _scoring(label: str, score: float) -> ScoringResult:
    ct = _ct(label)
    top = ScoredContentType(content_type=ct, score=score)
    return ScoringResult(top=top, candidates=[top])


FALLBACK = _ct("unknown")


# ---------------------------------------------------------------------------
# LabelingConfig
# ---------------------------------------------------------------------------

class TestLabelingConfig:
    def test_defaults(self):
        cfg = LabelingConfig()
        assert cfg.mode == PredictionMode.HIGH_CONFIDENCE
        assert isinstance(cfg.threshold, ThresholdConfig)

    def test_custom_mode(self):
        cfg = LabelingConfig(mode=PredictionMode.BEST_GUESS)
        assert cfg.mode == PredictionMode.BEST_GUESS

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match="Unknown prediction mode"):
            LabelingConfig(mode="nonsense")


# ---------------------------------------------------------------------------
# assign_label
# ---------------------------------------------------------------------------

class TestAssignLabel:
    def test_best_guess_always_returns_top(self):
        scoring = _scoring("python", score=0.1)  # very low score
        cfg = LabelingConfig(mode=PredictionMode.BEST_GUESS)
        result = assign_label(scoring, FALLBACK, cfg)
        assert result.label == "python"

    def test_high_confidence_above_threshold(self):
        threshold = ThresholdConfig(high=0.9, medium=0.7)
        cfg = LabelingConfig(mode=PredictionMode.HIGH_CONFIDENCE, threshold=threshold)
        scoring = _scoring("python", score=0.95)
        result = assign_label(scoring, FALLBACK, cfg)
        assert result.label == "python"

    def test_high_confidence_below_threshold_uses_fallback(self):
        threshold = ThresholdConfig(high=0.9, medium=0.7)
        cfg = LabelingConfig(mode=PredictionMode.HIGH_CONFIDENCE, threshold=threshold)
        scoring = _scoring("python", score=0.5)
        result = assign_label(scoring, FALLBACK, cfg)
        assert result.label == FALLBACK.label

    def test_medium_confidence_above_medium_threshold(self):
        threshold = ThresholdConfig(high=0.9, medium=0.6)
        cfg = LabelingConfig(mode=PredictionMode.MEDIUM_CONFIDENCE, threshold=threshold)
        scoring = _scoring("javascript", score=0.75)
        result = assign_label(scoring, FALLBACK, cfg)
        assert result.label == "javascript"

    def test_medium_confidence_below_medium_threshold_uses_fallback(self):
        threshold = ThresholdConfig(high=0.9, medium=0.6)
        cfg = LabelingConfig(mode=PredictionMode.MEDIUM_CONFIDENCE, threshold=threshold)
        scoring = _scoring("javascript", score=0.4)
        result = assign_label(scoring, FALLBACK, cfg)
        assert result.label == FALLBACK.label

    def test_default_config_used_when_none(self):
        scoring = _scoring("pdf", score=1.0)
        result = assign_label(scoring, FALLBACK, config=None)
        assert result.label == "pdf"
