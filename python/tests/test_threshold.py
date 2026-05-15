"""Tests for magika.threshold module."""

from __future__ import annotations

import pytest

from magika.threshold import (
    DEFAULT_THRESHOLD_CONFIG,
    ThresholdConfig,
    DEFAULT_HIGH_CONFIDENCE_THRESHOLD,
    DEFAULT_MEDIUM_CONFIDENCE_THRESHOLD,
    DEFAULT_LOW_CONFIDENCE_THRESHOLD,
)


class TestThresholdConfig:
    def test_defaults(self):
        cfg = ThresholdConfig()
        assert cfg.high == DEFAULT_HIGH_CONFIDENCE_THRESHOLD
        assert cfg.medium == DEFAULT_MEDIUM_CONFIDENCE_THRESHOLD
        assert cfg.low == DEFAULT_LOW_CONFIDENCE_THRESHOLD

    def test_custom_valid(self):
        cfg = ThresholdConfig(high=0.85, medium=0.65, low=0.45)
        assert cfg.high == 0.85

    def test_out_of_range_raises(self):
        with pytest.raises(ValueError, match="'high'"):
            ThresholdConfig(high=1.5)

    def test_ordering_violation_raises(self):
        with pytest.raises(ValueError, match="low <= medium <= high"):
            ThresholdConfig(high=0.5, medium=0.8, low=0.3)

    def test_classify_high(self):
        cfg = ThresholdConfig()
        assert cfg.classify_score(0.95) == "high"

    def test_classify_medium(self):
        cfg = ThresholdConfig()
        assert cfg.classify_score(0.75) == "medium"

    def test_classify_low(self):
        cfg = ThresholdConfig()
        assert cfg.classify_score(0.55) == "low"

    def test_classify_unknown(self):
        cfg = ThresholdConfig()
        assert cfg.classify_score(0.1) == "unknown"

    def test_classify_boundary_high(self):
        cfg = ThresholdConfig()
        assert cfg.classify_score(0.9) == "high"

    def test_frozen(self):
        cfg = ThresholdConfig()
        with pytest.raises((AttributeError, TypeError)):
            cfg.high = 0.5  # type: ignore[misc]


def test_default_threshold_config_is_threshold_config():
    assert isinstance(DEFAULT_THRESHOLD_CONFIG, ThresholdConfig)
