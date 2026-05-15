"""Utilities for reading byte buffers and files for feature extraction."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Union

from magika.features import BEG_SIZE, END_SIZE, FileFeatures, extract_features

# Maximum bytes we need to read from a file to build features.
_READ_SIZE: int = BEG_SIZE + END_SIZE


def features_from_path(path: Union[str, os.PathLike]) -> FileFeatures:
    """Read *path* from disk and return its :class:`~magika.features.FileFeatures`.

    Only the first and last ``BEG_SIZE + END_SIZE`` bytes are read so that
    large files are handled efficiently.
    """
    path = Path(path)
    size = path.stat().st_size

    if size <= _READ_SIZE:
        data = path.read_bytes()
    else:
        with path.open("rb") as fh:
            beg_bytes = fh.read(BEG_SIZE)
            fh.seek(-END_SIZE, os.SEEK_END)
            end_bytes = fh.read(END_SIZE)
        # Reconstruct a virtual buffer so extract_features handles padding.
        data = beg_bytes + end_bytes

    return extract_features(data)


def features_from_bytes(data: bytes) -> FileFeatures:
    """Return :class:`~magika.features.FileFeatures` for an in-memory *data* buffer."""
    return extract_features(data)


def features_from_path_or_bytes(
    source: Union[str, os.PathLike, bytes],
) -> FileFeatures:
    """Convenience dispatcher: accepts a file path **or** raw bytes."""
    if isinstance(source, (str, os.PathLike)):
        return features_from_path(source)
    if isinstance(source, bytes):
        return features_from_bytes(source)
    raise TypeError(
        f"source must be a path (str/PathLike) or bytes, got {type(source).__name__!r}"
    )
