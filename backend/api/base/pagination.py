from rest_framework.pagination import PageNumberPagination

from . import constants


class CustomPageNumberPagination(PageNumberPagination):
    page_size = constants.PAGINATOR_PAGE_SIZE
    page_size_query_param = 'limit'
    max_page_size = constants.PAGINATOR_MAX_PAGE_SIZE
