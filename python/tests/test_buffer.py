"""Tests for python/magika/buffer.py."""

from __future__ import annotations

import pytest

from magika.buffer import (
    features_from_bytes,
    features_from_path,
    features_from_path_or_bytes,
)
from magika.features import BEG_SIZE, END_SIZE, PAD_VALUE, FileFeatures


class TestFeaturesFromBytes:
    def test_returns_file_features(self) -> None:
        ff = features_from_bytes(b"hello")
        assert isinstance(ff, FileFeatures)

    def test_empty_bytes_all_padded(self) -> None:
        ff = features_from_bytes(b"")
        assert all(v == PAD_VALUE for v in ff.beg)
        assert all(v == PAD_VALUE for v in ff.end)

    def test_known_prefix_preserved(self) -> None:
        data = bytes(range(10))
        ff = features_from_bytes(data)
        assert ff.beg[:10] == tuple(range(10))


class TestFeaturesFromPath:
    def test_small_file(self, tmp_path) -> None:
        p = tmp_path / "small.bin"
        p.write_bytes(b"\x00\x01\x02")
        ff = features_from_path(p)
        assert isinstance(ff, FileFeatures)
        assert ff.beg[:3] == (0, 1, 2)

    def test_large_file_beg_correct(self, tmp_path) -> None:
        # Write a file larger than BEG_SIZE + END_SIZE
        data = bytes(range(256)) * 8  # 2 048 bytes
        p = tmp_path / "large.bin"
        p.write_bytes(data)
        ff = features_from_path(p)
        assert ff.beg[:256] == tuple(range(256))

    def test_large_file_end_correct(self, tmp_path) -> None:
        data = b"\xff" * (BEG_SIZE + END_SIZE + 100)
        p = tmp_path / "large2.bin"
        p.write_bytes(data)
        ff = features_from_path(p)
        # Last END_SIZE bytes are all 0xff
        assert all(v == 0xFF for v in ff.end)

    def test_string_path_accepted(self, tmp_path) -> None:
        p = tmp_path / "str.bin"
        p.write_bytes(b"abc")
        ff = features_from_path(str(p))
        assert isinstance(ff, FileFeatures)


class TestFeaturesFromPathOrBytes:
    def test_bytes_input(self) -> None:
        ff = features_from_path_or_bytes(b"test")
        assert isinstance(ff, FileFeatures)

    def test_path_input(self, tmp_path) -> None:
        p = tmp_path / "dispatch.bin"
        p.write_bytes(b"data")
        ff = features_from_path_or_bytes(p)
        assert isinstance(ff, FileFeatures)

    def test_str_path_input(self, tmp_path) -> None:
        p = tmp_path / "dispatch_str.bin"
        p.write_bytes(b"data")
        ff = features_from_path_or_bytes(str(p))
        assert isinstance(ff, FileFeatures)

    def test_invalid_type_raises(self) -> None:
        with pytest.raises(TypeError, match="source must be"):
            features_from_path_or_bytes(12345)  # type: ignore[arg-type]
