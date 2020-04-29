# -*- coding: utf-8 -*-
# author: timor

from notices.models import *
from rest_framework import serializers


class MailBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailBot
        fields = '__all__'


class TelegramBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramBot
        fields = '__all__'
