# -*- coding: utf-8 -*-
# author: itimor

from itertools import chain
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

    def get_queryset(self):
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_admin:
                return Workflow.objects.all()
            else:
                user_roles = user.roles.all()
                group_roles = user.group.roles.all()
                all_roles = sorted(chain(user_roles, group_roles), key=lambda t: t.id, reverse=True)
                return Workflow.objects.filter(roles__in=all_roles).distinct()
        except Exception as e:
            print(e)
            return Workflow.objects.all()


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


class WorkflowBpmnViewSet(BulkModelMixin):
    queryset = WorkflowBpmn.objects.all()
    serializer_class = WorkflowBpmnSerializer
