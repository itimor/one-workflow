# -*- coding: utf-8 -*-
# author: itimor

from tickets.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin


class TicketViewSet(BulkModelMixin):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    search_fields = ['name']
    filter_fields = ['name', 'sn']
    ordering_fields = ['state']


class TicketFlowLogViewSet(BulkModelMixin):
    queryset = TicketFlowLog.objects.all()
    serializer_class = TicketFlowLogSerializer
    search_fields = ['ticket']
    filter_fields = ['ticket', 'state']


class TicketCustomFieldViewSet(BulkModelMixin):
    queryset = TicketCustomField.objects.all()
    serializer_class = TicketCustomFieldSerializer
    filter_fields = ['ticket_id', 'customfield_id']


class TicketUserViewSet(BulkModelMixin):
    queryset = TicketUser.objects.all()
    serializer_class = TicketUserSerializer
    search_fields = ['username']
    filter_fields = ['username']
