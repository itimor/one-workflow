# -*- coding: utf-8 -*-
# author: timor

from rest_framework import serializers
from tools.models import *


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = '__all__'


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'


class RequestEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestEvent
        fields = '__all__'

class SimpleSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = SimpleModel
        fields = '__all__'
