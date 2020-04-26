# -*- coding: utf-8 -*-
# author: itimor

from workflows.models import *
from rest_framework import serializers


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'


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
