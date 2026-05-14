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

"""Tests for the content_types module."""

import pytest

from magika.content_types import (
    ContentType,
    get_content_type,
    get_content_types_by_group,
    list_content_types,
)


class TestContentType:
    def test_str_returns_label(self):
        ct = ContentType(label="python", mime_type="text/x-python", group="code", description="Python")
        assert str(ct) == "python"

    def test_repr_contains_label_and_mime(self):
        ct = ContentType(label="json", mime_type="application/json", group="data", description="JSON")
        assert "json" in repr(ct)
        assert "application/json" in repr(ct)

    def test_default_extensions_is_empty_list(self):
        ct = ContentType(label="x", mime_type="x/x", group="x", description="x")
        assert ct.extensions == []

    def test_default_is_text_is_false(self):
        ct = ContentType(label="x", mime_type="x/x", group="x", description="x")
        assert ct.is_text is False


class TestGetContentType:
    def test_returns_known_type(self):
        ct = get_content_type("python")
        assert ct is not None
        assert ct.label == "python"
        assert ct.mime_type == "text/x-python"

    def test_returns_none_for_unknown_label(self):
        assert get_content_type("nonexistent_type_xyz") is None

    def test_unknown_sentinel_type(self):
        ct = get_content_type("unknown")
        assert ct is not None
        assert ct.mime_type == "application/octet-stream"


class TestListContentTypes:
    def test_returns_list(self):
        result = list_content_types()
        assert isinstance(result, list)

    def test_list_is_non_empty(self):
        assert len(list_content_types()) > 0

    def test_all_items_are_content_type_instances(self):
        for ct in list_content_types():
            assert isinstance(ct, ContentType)


class TestGetContentTypesByGroup:
    def test_returns_code_types(self):
        code_types = get_content_types_by_group("code")
        labels = [ct.label for ct in code_types]
        assert "python" in labels
        assert "javascript" in labels

    def test_returns_empty_for_nonexistent_group(self):
        assert get_content_types_by_group("nonexistent_group") == []

    def test_all_returned_types_match_group(self):
        for ct in get_content_types_by_group("image"):
            assert ct.group == "image"
