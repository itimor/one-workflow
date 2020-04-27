# -*- coding: utf-8 -*-
# author: itimor

from __future__ import print_function, unicode_literals

import json
from rest_framework.response import Response
from collections import OrderedDict
from rest_framework import viewsets
from django.utils import timezone
from rest_framework.decorators import action
from common import status
from common.dispath import JsonResponse
from common.exceptions import *
from tools.models import RequestEvent


class ModelViewSet(viewsets.ModelViewSet):

    def __init__(self, *args, **kwargs):
        super(ModelViewSet, self).__init__(*args, **kwargs)
        self.resultData = False

    def watch_audit_log(self, request):

        ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if not ip:
            ip = request.META.get('REMOTE_ADDR', "")
        method = request._request.method
        RequestEvent.objects.create(
            url=request.path,
            method=method,
            query_string=json.dumps({
                'query_params': request.query_params,
                'json': request.data
            }),
            user=self.request.user,
            remote_ip=ip,
            create_time=timezone.now()
        )

    def create(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return JsonResponse(OrderedDict([
                ('results', serializer.data)
            ], code=status.HTTP_200_OK), headers=headers)
        except Exception as e:
            print(e)
            return JsonResponse(OrderedDict([
                ('results', {"msg": ExceptionX.PasreRaise(e)})
            ], code=status.HTTP_500_INTERNAL_SERVER_ERROR))

    def perform_create(self, serializer):
        serializer.save()

    def list(self, request, *args, **kwargs):
        # 不记录list get请求
        # self.watch_audit_log(request)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(OrderedDict([
            ('results', serializer.data)
        ], code=status.HTTP_200_OK))

    def retrieve(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(OrderedDict([
            ('results', serializer.data)
        ], code=status.HTTP_200_OK))

    def update(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(OrderedDict([
            ('results', serializer.data)
        ], code=status.HTTP_200_OK))

    def perform_update(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(OrderedDict(code=status.HTTP_200_OK))

    def perform_destroy(self, instance):
        instance.delete()


class FKModelViewSet(ModelViewSet):

    def transer(self, instance=None, id=None):
        self.resultData = True
        if self.action == "create":
            self.kwargs = {'pk': id}
            instance = self.get_object()
        serializer = self.get_serializer(instance)
        return serializer

    def perform_create(self, serializer):
        super(FKModelViewSet, self).perform_create(serializer)
        self.readSerializer = self.transer(id=serializer.data['id'])

    def perform_update(self, serializer):
        super(FKModelViewSet, self).perform_update(serializer)
        self.readSerializer = self.transer(self.readInstance)

    def perform_destroy(self, instance):
        super(FKModelViewSet, self).perform_destroy(instance)

    def create(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = self.readSerializer
        return JsonResponse(OrderedDict([
            ('results', serializer.data)
        ], code=status.HTTP_200_OK), headers=headers)

    def update(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        partial = kwargs.pop('partial', False)
        self.readInstance = instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = self.readSerializer

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return JsonResponse(OrderedDict([
            ('results', serializer.data)
        ], code=status.HTTP_200_OK))

    def destroy(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(OrderedDict(code=status.HTTP_200_OK))


# 批量操作modelview  bulk_create|bulk_delete|bulk_update
class BulkModelMixin(ModelViewSet):
    # 批量添加
    @action(methods=['post'], url_path='bulk_create', detail=False)
    def bulk_create(self, request, *args, **kwargs):
        """
        /api/tool/simple/bulk_create/
        :return:
        """
        self.watch_audit_log(request)
        objs = request.data

        if not objs:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        bulk_models = []
        for obj in objs:
            req = {'id': '0102', 'msg': 'success'}
            print(obj)
            try:
                serializer = self.get_serializer(data=obj)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                req['id'] = serializer.data['id']
            except Exception as e:
                req['msg'] = ExceptionX.ToString(e)

            bulk_models.append(req)

        return JsonResponse(OrderedDict([
            ('results', bulk_models)
        ], code=status.HTTP_200_OK))

    @action(methods=['delete'], url_path='bulk_delete', detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        """
        /api/tool/simple/bulk_delete/
        :return:
        """
        self.watch_audit_log(request)
        ids = request.data

        if not ids:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bulk_models = []
        for id in ids:
            req = {'id': id, 'msg': 'success'}
            try:
                queryset = self.filter_queryset(self.get_queryset())
                instance = queryset.get(pk=id)
                self.perform_destroy(instance)
            except Exception as e:
                req['msg'] = ExceptionX.ToString(e)

            bulk_models.append(req)

        return JsonResponse(OrderedDict([
            ('results', bulk_models)
        ], code=status.HTTP_200_OK))

    @action(methods=['put', 'patch'], url_path='bulk_update', detail=False)
    def bulk_update(self, request, *args, **kwargs):
        """
        /api/tool/simple/bulk_update/
        :return:
        """
        self.watch_audit_log(request)
        ids = request.data['ids']
        obj = request.data['obj']

        if not ids or not obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        bulk_models = []
        for id in ids:
            req = {'id': id, 'msg': 'success'}
            try:
                queryset = self.filter_queryset(self.get_queryset())
                instance = queryset.get(pk=id)
                serializer = self.get_serializer(instance, data=obj, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
            except Exception as e:
                req['msg'] = ExceptionX.ToString(e)

            bulk_models.append(req)

        return JsonResponse(OrderedDict([
            ('results', bulk_models)
        ], code=status.HTTP_200_OK))
