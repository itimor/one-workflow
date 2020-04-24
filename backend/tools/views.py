# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets, permissions
from tools.models import *
from tools.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin


class UploadViewSet(ModelViewSet):
    queryset = Upload.objects.all().order_by("-create_time")
    serializer_class = UploadSerializer
    filter_fields = ('username', 'type',)


class FileUploadViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer


class RequestEventViewSet(ModelViewSet):
    queryset = RequestEvent.objects.all()
    serializer_class = RequestEventSerializer
    search_fields = ['url', 'query_string', 'user', 'remote_ip']
    filter_fields = ['method']


class SimpleViewSet(BulkModelMixin):
    queryset = SimpleModel.objects.all()
    serializer_class = SimpleSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = ['id', 'name']

