"""Feature extraction utilities for Magika content-type detection."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

# Number of bytes sampled from the beginning and end of a file.
BEG_SIZE: int = 512
END_SIZE: int = 512

# Byte value used to pad sequences that are shorter than the required length.
PAD_VALUE: int = 256  # out-of-byte-range sentinel


@dataclass(frozen=True)
class FileFeatures:
    """Raw byte features extracted from a file or buffer."""

    beg: tuple[int, ...]
    end: tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.beg) != BEG_SIZE:
            raise ValueError(
                f"beg must have exactly {BEG_SIZE} elements, got {len(self.beg)}"
            )
        if len(self.end) != END_SIZE:
            raise ValueError(
                f"end must have exactly {END_SIZE} elements, got {len(self.end)}"
            )
        for val in (*self.beg, *self.end):
            if not (0 <= val <= PAD_VALUE):
                raise ValueError(
                    f"byte values must be in [0, {PAD_VALUE}], got {val}"
                )

    @property
    def flat(self) -> tuple[int, ...]:
        """Concatenated beg + end feature vector."""
        return self.beg + self.end


def _pad(seq: Sequence[int], size: int) -> tuple[int, ...]:
    """Right-pad *seq* with PAD_VALUE up to *size* elements."""
    seq = tuple(seq[:size])
    return seq + (PAD_VALUE,) * (size - len(seq))


def extract_features(data: bytes) -> FileFeatures:
    """Extract :class:`FileFeatures` from raw *data* bytes."""
    beg = _pad(data[:BEG_SIZE], BEG_SIZE)
    end = _pad(data[-END_SIZE:] if len(data) > END_SIZE else data, END_SIZE)
    return FileFeatures(beg=beg, end=end)
