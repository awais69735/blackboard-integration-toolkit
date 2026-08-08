"""Pagination handling for Blackboard API."""

from typing import TypeVar, Generic, Iterator, Optional, Dict, Any, List
from blackboard.interfaces.config.settings import PaginationSettings

T = TypeVar("T")


class PageIterator(Generic[T]):
    """Iterator for paginated results from Blackboard.

    Handles offset/limit pagination. It yields items from the current page and
    automatically fetches subsequent pages until the end.
    """

    def __init__(
        self,
        fetch_page_func,
        limit: Optional[int] = None,
        settings: Optional[PaginationSettings] = None,
        **filters
    ):
        """
        Args:
            fetch_page_func: A callable that takes (limit, offset, **filters) and returns
                             a tuple of (items, total_count) or (items, next_offset).
                             We'll assume it returns (items, total_count).
            limit: Items per page. If None, use default from settings.
            settings: PaginationSettings instance.
            filters: Additional filters passed to fetch_page_func.
        """
        self._fetch_page = fetch_page_func
        self._settings = settings or PaginationSettings()
        self._limit = limit or self._settings.default_limit
        if self._limit > self._settings.max_limit:
            self._limit = self._settings.max_limit
        self._filters = filters
        self._offset = 0
        self._total: Optional[int] = None
        self._items: List[T] = []
        self._index = 0
        self._exhausted = False

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self._exhausted:
            raise StopIteration
        if self._index >= len(self._items):
            # Need to fetch next page
            if self._total is not None and self._offset >= self._total:
                self._exhausted = True
                raise StopIteration
            # Fetch page
            items, total = self._fetch_page(self._limit, self._offset, **self._filters)
            self._items = items
            self._total = total
            self._index = 0
            if not items:
                self._exhausted = True
                raise StopIteration
            self._offset += self._limit
        item = self._items[self._index]
        self._index += 1
        return item