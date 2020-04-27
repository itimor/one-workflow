# -*- coding: utf-8 -*-
# author: itimor

from tickets.models import *
from workflows.models import *
from systems.models import User
from rest_framework import serializers
from utils.index import gen_time_pid
import json


class TicketReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
        depth = 1


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

    def create(self, validated_data):
        workflow = validated_data["workflow"]
        transition = validated_data["transition"]
        state = validated_data["state"]
        customfield_list = validated_data["customfield"]

        # save ticket
        validated_data["sn"] = gen_time_pid(workflow.ticket_sn_prefix)
        ticket = Ticket.objects.create(**validated_data)

        # save ticketlog
        ticketlog = dict()
        ticketlog["ticket"] = ticket
        ticketlog["state"] = state
        ticketlog["transition"] = transition
        ticketlog["participant"] = state.participant
        ticketlog["participant_type"] = state.participant_type
        TicketFlowLog.objects.create(**ticketlog)

        # save customfield
        field_models = []
        for customfield in json.loads(customfield_list):
            field_models.append(
                TicketCustomField(ticket=ticket, customfield_id=int(customfield['id']),
                                  field_value=customfield['field_value']))
        TicketCustomField.objects.bulk_create(field_models)

        # save ticketuser
        user1 = User.objects.get(username=validated_data["create_user"])
        user2 = User.objects.get(username=state.participant)
        TicketUser.objects.create(ticket=ticket, username=user1, worked=True)
        TicketUser.objects.create(ticket=ticket, username=user2, in_process=True)

        return ticket

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.workflow = validated_data.get('workflow', instance.workflow)
        instance.sn = validated_data.get('sn', instance.sn)
        instance.state = validated_data.get('state', instance.state)
        instance.create_user = validated_data.get('create_user', instance.create_user)
        instance.transition = validated_data.get('transition', instance.transition)
        instance.customfield = validated_data.get('customfield', instance.customfield)
        instance.save()

        # save ticketuser
        print(instance.state)
        # user1 = User.objects.get(username=validated_data["create_user"])
        # user2 = User.objects.get(username=state.participant)
        # TicketUser.objects.create(ticket=ticket, username=user1, worked=True)
        # TicketUser.objects.create(ticket=ticket, username=user2, in_process=True)
        return instance


class TicketFlowLogReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFlowLog
        fields = '__all__'
        depth = 1


class TicketFlowLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFlowLog
        fields = '__all__'


class TicketCustomFieldReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCustomField
        fields = '__all__'
        depth = 1


class TicketCustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCustomField
        fields = '__all__'


class TicketUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketUser
        fields = '__all__'
