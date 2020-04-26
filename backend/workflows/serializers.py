# -*- coding: utf-8 -*-
# author: itimor

from workflows.models import *
from rest_framework import serializers


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'

    def create(self, validated_data):
        obj = Workflow.objects.create(**validated_data)
        obj.save()
        State.objects.create(name="发起人-新建中", order_id=1, state_type=1, workflow=obj)
        State.objects.create(name="结束", order_id=99, state_type=2, workflow=obj)
        return obj


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'


class TransitionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = '__all__'
        depth = 1


class TransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transition
        fields = '__all__'


class CustomFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomField
        fields = '__all__'
