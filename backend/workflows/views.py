# -*- coding: utf-8 -*-
# author: itimor

from workflows.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin


class WorkflowTypeViewSet(BulkModelMixin):
    queryset = WorkflowType.objects.all()
    serializer_class = WorkflowTypeSerializer
    search_fields = ['name']
    filter_fields = ['name', 'code', 'status']


class WorkflowViewSet(BulkModelMixin):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    search_fields = ['name']
    filter_fields = ['name', 'id', 'type']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return WorkflowReadSerializer
        return WorkflowSerializer


class StateViewSet(BulkModelMixin):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    search_fields = ['name']
    filter_fields = ['workflow', 'is_hidden']
    ordering_fields = ['state_type', 'order_id']


class TransitionViewSet(BulkModelMixin):
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    search_fields = ['name']
    filter_fields = ['workflow', 'transition_type', 'source_state', 'dest_state']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return TransitionReadSerializer
        return TransitionSerializer


class CustomFieldViewSet(BulkModelMixin):
    queryset = CustomField.objects.all()
    serializer_class = CustomFieldSerializer
    search_fields = ['field_name']
    filter_fields = ['workflow', 'field_type', 'field_attribute']
    ordering_fields = ['field_type', 'order_id']
