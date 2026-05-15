"""Magika — ML-based file type detection."""

from magika.content_types import ContentType, get_content_type, list_content_types
from magika.prediction import PredictionMode, PredictionResult
from magika.scorer import ScoredContentType, ScoringResult
from magika.threshold import ThresholdConfig

__all__ = [
    "ContentType",
    "get_content_type",
    "list_content_types",
    "PredictionMode",
    "PredictionResult",
    "ScoredContentType",
    "ScoringResult",
    "ThresholdConfig",
]

__version__ = "0.1.0"
