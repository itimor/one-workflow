# -*- coding: utf-8 -*-
# author: itimor

from tickets.models import *
from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class TicketFlowLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFlowLog
        fields = '__all__'


class TicketCustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCustomField
        fields = '__all__'


class TicketUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketUser
        fields = '__all__'
