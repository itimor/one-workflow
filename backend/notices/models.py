# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from common.models import BaseModel

notice_type = {
    'mail': 'mail',
    'telegram': 'telegram',
}


class MailBot(BaseModel):
    type = models.CharField(max_length=10, choices=tuple(notice_type.items()), default=0, verbose_name='通知类型')
    name = models.CharField(max_length=112, unique=True, verbose_name='名称')
    host = models.CharField(max_length=112, verbose_name='主机')
    user = models.CharField(max_length=112, verbose_name='账号')
    password = models.CharField(max_length=112, verbose_name='密码')
    to = models.CharField(max_length=112, verbose_name='接收者')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "邮件机器人"
        verbose_name_plural = verbose_name


class TelegramBot(BaseModel):
    type = models.CharField(max_length=10, choices=tuple(notice_type.items()), default=0, verbose_name='通知类型')
    name = models.CharField(max_length=112, unique=True, verbose_name='名称')
    uid = models.CharField(max_length=112, verbose_name='账号id')
    token = models.CharField(max_length=112, verbose_name='token')
    chat_id = models.CharField(max_length=112, verbose_name='chat_id')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "tg机器人"
        verbose_name_plural = verbose_name
