from rest_framework.pagination import CursorPagination


class TutorialArticlesPaginator(CursorPagination):
    page_size = 20
    ordering = 'order'
