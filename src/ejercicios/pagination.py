from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class ProductPagination(PageNumberPagination):
    page_query_param = "p"
    page_size_query_param = "size"
    max_page_size = 5
    last_page_strings = "end"

class ProductLOPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "sz"
    offset_query_param = "pg"
    max_limit = 5