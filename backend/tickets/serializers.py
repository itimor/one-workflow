# -*- coding: utf-8 -*-
# author: itimor

from tickets.models import *
from workflows.models import *
from rest_framework import serializers
from utils.index import gen_time_pid

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        workflow = validated_data["workflow"]
        validated_data["sn"] = gen_time_pid(workflow.ticket_sn_prefix)
        ticket = Ticket.objects.create(**validated_data)
        ticket.save()
        return ticket


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
