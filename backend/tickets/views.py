# -*- coding: utf-8 -*-
# author: itimor

from tickets.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin


class TicketViewSet(BulkModelMixin):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    search_fields = ['name']
    filter_fields = ['name', 'id', 'create_user']
    ordering_fields = ['state']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return TicketReadSerializer
        return TicketSerializer


class TicketFlowLogViewSet(BulkModelMixin):
    queryset = TicketFlowLog.objects.all()
    serializer_class = TicketFlowLogSerializer
    search_fields = ['ticket']
    filter_fields = ['ticket', 'state']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return TicketFlowLogReadSerializer
        return TicketFlowLogSerializer


class TicketCustomFieldViewSet(BulkModelMixin):
    queryset = TicketCustomField.objects.all()
    serializer_class = TicketCustomFieldSerializer
    filter_fields = ['ticket', 'customfield']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return TicketCustomFieldReadSerializer
        return TicketCustomFieldSerializer


class TicketUserViewSet(BulkModelMixin):
    queryset = TicketUser.objects.all()
    serializer_class = TicketUserSerializer
    search_fields = ['username']
    filter_fields = ['username__username', 'in_process', 'worked']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return TicketUserReadSerializer
        return TicketUserSerializer
