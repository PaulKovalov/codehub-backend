from rest_framework.pagination import CursorPagination


class DefaultPaginator(CursorPagination):
    page_size = 20
    ordering = '-date_created'
