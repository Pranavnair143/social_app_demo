from drf_multiple_model.pagination import MultipleModelLimitOffsetPagination


class PostPagination(MultipleModelLimitOffsetPagination):
    default_limit = 10
