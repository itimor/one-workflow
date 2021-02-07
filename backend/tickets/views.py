# -*- coding: utf-8 -*-
# author: itimor

from tickets.serializers import *
from tickets.filters import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin


class TicketViewSet(BulkModelMixin):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filterset_class = TicketFilter
    search_fields = ['name']
    ordering_fields = ['state']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return TicketReadSerializer
        return TicketSerializer

    def get_queryset(self):
        try:
            user = User.objects.get(username=self.request.user)
            if user.is_admin:
                return Ticket.objects.all()
            else:
                return Ticket.objects.filter(relation__icontains=self.request.user).distinct()
        except Exception as e:
            print(e)
            return Ticket.objects.all()


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
    filter_fields = ['username', 'in_process', 'worked']
