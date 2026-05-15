"""Tests for python/magika/features.py."""

from __future__ import annotations

import pytest

from magika.features import (
    BEG_SIZE,
    END_SIZE,
    PAD_VALUE,
    FileFeatures,
    _pad,
    extract_features,
)


# ---------------------------------------------------------------------------
# _pad helpers
# ---------------------------------------------------------------------------

class TestPad:
    def test_shorter_than_size(self) -> None:
        result = _pad([1, 2, 3], 6)
        assert result == (1, 2, 3, PAD_VALUE, PAD_VALUE, PAD_VALUE)

    def test_exact_size(self) -> None:
        result = _pad([1, 2], 2)
        assert result == (1, 2)

    def test_longer_than_size_truncated(self) -> None:
        result = _pad([1, 2, 3, 4], 2)
        assert result == (1, 2)

    def test_empty_input(self) -> None:
        result = _pad([], 3)
        assert result == (PAD_VALUE, PAD_VALUE, PAD_VALUE)


# ---------------------------------------------------------------------------
# FileFeatures dataclass
# ---------------------------------------------------------------------------

def _make_vector(size: int, fill: int = 0) -> tuple[int, ...]:
    return tuple([fill] * size)


class TestFileFeatures:
    def test_valid_construction(self) -> None:
        beg = _make_vector(BEG_SIZE, 1)
        end = _make_vector(END_SIZE, 2)
        ff = FileFeatures(beg=beg, end=end)
        assert len(ff.beg) == BEG_SIZE
        assert len(ff.end) == END_SIZE

    def test_flat_is_concatenation(self) -> None:
        beg = _make_vector(BEG_SIZE, 10)
        end = _make_vector(END_SIZE, 20)
        ff = FileFeatures(beg=beg, end=end)
        assert ff.flat == beg + end
        assert len(ff.flat) == BEG_SIZE + END_SIZE

    def test_wrong_beg_length_raises(self) -> None:
        with pytest.raises(ValueError, match="beg"):
            FileFeatures(beg=(0,) * (BEG_SIZE - 1), end=_make_vector(END_SIZE))

    def test_wrong_end_length_raises(self) -> None:
        with pytest.raises(ValueError, match="end"):
            FileFeatures(beg=_make_vector(BEG_SIZE), end=(0,) * (END_SIZE + 1))

    def test_out_of_range_byte_raises(self) -> None:
        bad_beg = _make_vector(BEG_SIZE - 1) + (300,)
        with pytest.raises(ValueError, match="byte values"):
            FileFeatures(beg=bad_beg, end=_make_vector(END_SIZE))

    def test_pad_value_is_allowed(self) -> None:
        beg = _make_vector(BEG_SIZE, PAD_VALUE)
        end = _make_vector(END_SIZE, PAD_VALUE)
        ff = FileFeatures(beg=beg, end=end)
        assert ff.beg[0] == PAD_VALUE


# ---------------------------------------------------------------------------
# extract_features
# ---------------------------------------------------------------------------

class TestExtractFeatures:
    def test_empty_bytes(self) -> None:
        ff = extract_features(b"")
        assert len(ff.beg) == BEG_SIZE
        assert len(ff.end) == END_SIZE
        assert all(v == PAD_VALUE for v in ff.beg)
        assert all(v == PAD_VALUE for v in ff.end)

    def test_short_data_beg_equals_end(self) -> None:
        data = b"hello"
        ff = extract_features(data)
        assert ff.beg[:5] == tuple(data)
        assert ff.end[:5] == tuple(data)

    def test_long_data_beg_and_end_differ(self) -> None:
        data = bytes(range(256)) * 8  # 2048 bytes
        ff = extract_features(data)
        assert ff.beg[:256] == tuple(range(256))
        # end should reflect the last END_SIZE bytes
        expected_end_start = tuple(data[-END_SIZE:][:4])
        assert ff.end[:4] == expected_end_start

    def test_returns_file_features_instance(self) -> None:
        ff = extract_features(b"abc")
        assert isinstance(ff, FileFeatures)
