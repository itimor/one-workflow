# -*- coding: utf-8 -*-
# author: itimor

from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from common import status
from common.dispath import JsonResponse


def _positive_int(integer_string, strict=False, cutoff=None):
    """
    分页大小为零不分页
    """
    ret = int(integer_string)
    if ret < 0:
        raise ValueError()
    if (ret == 0) and strict:
        return None
    if cutoff:
        return min(ret, cutoff)
    return ret


class StandardResultsSetPagination(PageNumberPagination):
    """
    配置分页规则
    """
    page_size = 20
    page_size_query_param = 'limit'
    page_query_param = 'page'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return JsonResponse(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ], code=status.HTTP_200_OK))

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                return _positive_int(
                    request.query_params[self.page_size_query_param],
                    strict=True,
                    cutoff=self.max_page_size
                )
            except (KeyError, ValueError):
                return None
        return self.page_size


class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_offset(self, request):
        try:
            return (int(request.query_params['offset']) - 1) * int(request.query_params['limit'])
        except (KeyError, ValueError):
            return 1
