# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Content type definitions and registry for Magika."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ContentType:
    """Represents a detectable content type."""

    label: str
    mime_type: str
    group: str
    description: str
    extensions: List[str] = field(default_factory=list)
    is_text: bool = False

    def __str__(self) -> str:
        return self.label

    def __repr__(self) -> str:
        return f"ContentType(label={self.label!r}, mime_type={self.mime_type!r})"


CONTENT_TYPES: Dict[str, ContentType] = {
    "python": ContentType(
        label="python",
        mime_type="text/x-python",
        group="code",
        description="Python source code",
        extensions=[".py", ".pyw"],
        is_text=True,
    ),
    "javascript": ContentType(
        label="javascript",
        mime_type="application/javascript",
        group="code",
        description="JavaScript source code",
        extensions=[".js", ".mjs"],
        is_text=True,
    ),
    "json": ContentType(
        label="json",
        mime_type="application/json",
        group="data",
        description="JSON data",
        extensions=[".json"],
        is_text=True,
    ),
    "pdf": ContentType(
        label="pdf",
        mime_type="application/pdf",
        group="document",
        description="PDF document",
        extensions=[".pdf"],
        is_text=False,
    ),
    "png": ContentType(
        label="png",
        mime_type="image/png",
        group="image",
        description="PNG image",
        extensions=[".png"],
        is_text=False,
    ),
    "unknown": ContentType(
        label="unknown",
        mime_type="application/octet-stream",
        group="unknown",
        description="Unknown content type",
        extensions=[],
        is_text=False,
    ),
}


def get_content_type(label: str) -> Optional[ContentType]:
    """Retrieve a ContentType by its label."""
    return CONTENT_TYPES.get(label)


def list_content_types() -> List[ContentType]:
    """Return all registered content types."""
    return list(CONTENT_TYPES.values())


def get_content_types_by_group(group: str) -> List[ContentType]:
    """Return all content types belonging to a given group."""
    return [ct for ct in CONTENT_TYPES.values() if ct.group == group]
