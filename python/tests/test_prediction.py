"""Tests for magika.prediction module."""

from __future__ import annotations

from pathlib import Path

import pytest

from magika.content_types import ContentType
from magika.prediction import PredictionMode, PredictionResult
from magika.scorer import ScoredContentType, ScoringResult
from magika.threshold import ThresholdConfig


def _make_ct(label: str = "txt") -> ContentType:
    return ContentType(
        label=label,
        mime_type="text/plain",
        group="text",
        description="Plain text",
        extensions=["txt"],
        is_text=True,
    )


def _make_scoring_result(score: float = 0.99) -> ScoringResult:
    ct = _make_ct()
    scored = ScoredContentType(content_type=ct, score=score)
    threshold = ThresholdConfig()
    return ScoringResult(top=scored, overridden=None, threshold=threshold)


class TestPredictionMode:
    def test_constants_are_strings(self):
        assert isinstance(PredictionMode.HIGH_CONFIDENCE, str)
        assert isinstance(PredictionMode.BEST_GUESS, str)
        assert isinstance(PredictionMode.MAGIC_BYTES, str)

    def test_values_are_distinct(self):
        modes = [
            PredictionMode.HIGH_CONFIDENCE,
            PredictionMode.BEST_GUESS,
            PredictionMode.MAGIC_BYTES,
        ]
        assert len(set(modes)) == 3


class TestPredictionResult:
    def test_valid_high_confidence(self):
        result = PredictionResult(
            path=Path("file.txt"),
            dl=_make_scoring_result(0.99),
            output=_make_ct(),
            mode=PredictionMode.HIGH_CONFIDENCE,
        )
        assert result.is_high_confidence is True
        assert result.label == "txt"

    def test_valid_best_guess(self):
        result = PredictionResult(
            path=None,
            dl=_make_scoring_result(0.4),
            output=_make_ct(),
            mode=PredictionMode.BEST_GUESS,
        )
        assert result.is_high_confidence is False

    def test_valid_magic_bytes(self):
        result = PredictionResult(
            path=Path("file.txt"),
            dl=_make_scoring_result(0.5),
            output=_make_ct(),
            mode=PredictionMode.MAGIC_BYTES,
        )
        assert result.mode == PredictionMode.MAGIC_BYTES

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match="mode must be one of"):
            PredictionResult(
                path=None,
                dl=_make_scoring_result(),
                output=_make_ct(),
                mode="unknown_mode",
            )

    def test_invalid_path_type_raises(self):
        with pytest.raises(TypeError, match="path must be a Path or None"):
            PredictionResult(
                path="not_a_path",  # type: ignore[arg-type]
                dl=_make_scoring_result(),
                output=_make_ct(),
                mode=PredictionMode.HIGH_CONFIDENCE,
            )

    def test_none_path_allowed(self):
        result = PredictionResult(
            path=None,
            dl=_make_scoring_result(),
            output=_make_ct(),
            mode=PredictionMode.HIGH_CONFIDENCE,
        )
        assert result.path is None

    def test_repr_contains_label_and_mode(self):
        result = PredictionResult(
            path=Path("sample.txt"),
            dl=_make_scoring_result(0.95),
            output=_make_ct("txt"),
            mode=PredictionMode.HIGH_CONFIDENCE,
        )
        r = repr(result)
        assert "txt" in r
        assert "high_confidence" in r
        assert "0.9500" in r
