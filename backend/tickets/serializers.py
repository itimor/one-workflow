# -*- coding: utf-8 -*-
# author: itimor

from tickets.models import *
from workflows.models import *
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
        cur_user = self.context['request'].user

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
        ticketlog["state"] = transition.source_state
        ticketlog["transition"] = transition
        ticketlog["participant"] = cur_user
        TicketFlowLog.objects.create(**ticketlog)

        # save customfield
        field_models = []
        for item in json.loads(customfield_list):
            if item['field_key'] == "create_user":
                field_models.append(
                    TicketCustomField(ticket=ticket, customfield_id=int(item['customfield']),
                                      field_value=ticket.create_user),
                )
            elif item['field_key'] == "create_time":
                field_models.append(
                    TicketCustomField(ticket=ticket, customfield_id=int(item['customfield']),
                                      field_value=ticket.create_time),
                )
            elif item['field_key'] == "group":
                field_models.append(
                    TicketCustomField(ticket=ticket, customfield_id=int(item['customfield']),
                                      field_value=ticket.create_user.group),
                )
            elif item['field_key'] == "id":
                field_models.append(
                    TicketCustomField(ticket=ticket, customfield_id=int(item['customfield']),
                                      field_value=ticket.create_user.id),
                )
            else:
                field_models.append(
                    TicketCustomField(ticket=ticket, customfield_id=int(item['customfield']),
                                      field_value=item['field_value'])
                )
        TicketCustomField.objects.bulk_create(field_models)

        # save ticketuser
        user2 = state.participant
        TicketUser.objects.create(ticket=ticket, username=cur_user, worked=True)
        TicketUser.objects.create(ticket=ticket, username=user2, in_process=True)

        return ticket

    def update(self, instance, validated_data):
        cur_user = self.context['request'].user
        instance.name = validated_data.get('name', instance.name)
        instance.workflow = validated_data.get('workflow', instance.workflow)
        instance.sn = validated_data.get('sn', instance.sn)
        instance.state = validated_data.get('state', instance.state)
        instance.create_user = validated_data.get('create_user', instance.create_user)
        instance.participant = validated_data.get('participant', instance.participant)
        instance.transition = validated_data.get('transition', instance.transition)
        instance.customfield = validated_data.get('customfield', instance.customfield)
        instance.save()

        # save ticketlog
        ticketlog = dict()
        ticketlog["ticket"] = instance
        ticketlog["state"] = instance.transition.source_state
        ticketlog["transition"] = instance.transition
        ticketlog["participant"] = cur_user
        TicketFlowLog.objects.create(**ticketlog)

        # save customfield
        customfield_list = json.loads(instance.customfield)
        for item in customfield_list:
            TicketCustomField.objects.filter(id=item["id"]).update(field_value=item["field_value"])

        # save ticketuser
        user2 = instance.state.participant
        TicketUser.objects.create(ticket=instance, username=cur_user, worked=True)
        TicketUser.objects.create(ticket=instance, username=user2, in_process=True)
        return instance


class TicketFlowLogReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketFlowLog
        fields = '__all__'
        depth = 2


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
