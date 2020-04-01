from rest_framework.pagination import CursorPagination


class ArticlePaginator(CursorPagination):
    page_size = 20
    ordering = '-date_created'
