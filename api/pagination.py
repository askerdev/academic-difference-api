"""Cursor pagination for API"""

from rest_framework.pagination import CursorPagination


class CursorPaginationWithOrdering(CursorPagination):
    ordering = "id"
