"""Unit tests for pagination iterator."""

from blackboard.infrastructure.http.pagination import PageIterator
from blackboard.interfaces.config.settings import PaginationSettings


class TestPageIterator:
    def test_iteration(self):
        def fake_fetch(limit, offset, **filters):
            # Return page of items and total
            total = 25
            items = list(range(offset, min(offset + limit, total)))
            return items, total

        settings = PaginationSettings(default_limit=10, max_limit=20)
        pager = PageIterator(fake_fetch, settings=settings)
        result = list(pager)
        assert result == list(range(25))