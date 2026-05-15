"""Tests for magika.scorer module."""

from __future__ import annotations

import pytest

from magika.content_types import ContentType
from magika.scorer import ScoredContentType, ScoringResult


def _make_ct(label: str) -> ContentType:
    return ContentType(
        label=label,
        mime_type=f"application/{label}",
        group="test",
        description=label.capitalize(),
        extensions=[],
        is_text=False,
    )


class TestScoredContentType:
    def test_valid_score_zero(self):
        ct = _make_ct("pdf")
        s = ScoredContentType(content_type=ct, score=0.0)
        assert s.score == 0.0

    def test_valid_score_one(self):
        ct = _make_ct("pdf")
        s = ScoredContentType(content_type=ct, score=1.0)
        assert s.score == 1.0

    def test_invalid_score_raises(self):
        ct = _make_ct("pdf")
        with pytest.raises(ValueError, match="Score must be between"):
            ScoredContentType(content_type=ct, score=1.5)

    def test_is_high_confidence_true(self):
        ct = _make_ct("pdf")
        s = ScoredContentType(content_type=ct, score=0.95)
        assert s.is_high_confidence is True

    def test_is_high_confidence_false(self):
        ct = _make_ct("pdf")
        s = ScoredContentType(content_type=ct, score=0.85)
        assert s.is_high_confidence is False

    def test_repr_contains_label_and_score(self):
        ct = _make_ct("pdf")
        s = ScoredContentType(content_type=ct, score=0.75)
        r = repr(s)
        assert "pdf" in r
        assert "0.7500" in r


class TestScoringResult:
    def _make_result(self) -> ScoringResult:
        candidates = [
            ScoredContentType(_make_ct("pdf"), 0.8),
            ScoredContentType(_make_ct("zip"), 0.95),
            ScoredContentType(_make_ct("txt"), 0.6),
        ]
        return ScoringResult(candidates=candidates)

    def test_top_returns_highest(self):
        result = self._make_result()
        assert result.top().content_type.label == "zip"

    def test_top_empty_returns_none(self):
        result = ScoringResult()
        assert result.top() is None

    def test_sorted_candidates_descending(self):
        result = self._make_result()
        scores = [c.score for c in result.sorted_candidates()]
        assert scores == sorted(scores, reverse=True)

    def test_filter_by_min_score(self):
        result = self._make_result()
        filtered = result.filter_by_min_score(0.75)
        assert len(filtered) == 2

    def test_len(self):
        result = self._make_result()
        assert len(result) == 3
