from rest_framework.pagination import CursorPagination


class AccountsPagination(CursorPagination):
    ordering = 'date_joined'
    page_size = 5
