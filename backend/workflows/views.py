# -*- coding: utf-8 -*-
# author: itimor

from workflows.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin


class WorkflowViewSet(BulkModelMixin):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    search_fields = ['name']
    filter_fields = ['name']


class StateViewSet(BulkModelMixin):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['type', 'order_id']


class TransitionViewSet(BulkModelMixin):
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    search_fields = ['name']
    filter_fields = ['name', 'type']
    ordering_fields = ['name']


class CustomFieldViewSet(BulkModelMixin):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    search_fields = ['field_name']
    filter_fields = ['field_type', 'field_type']
    ordering_fields = ['field_type', 'order_id']
