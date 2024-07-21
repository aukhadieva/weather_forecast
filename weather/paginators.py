from rest_framework import pagination


class WeatherPaginator(pagination.PageNumberPagination):
    """
    Пагинатор для вывода списка погоды.
    """

    page_size = 5
    page_query_param = "page_size"
    max_page_size = 50
