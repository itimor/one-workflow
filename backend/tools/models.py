# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from common.models import BaseModel
from tools.filesize import convert_size
from tools.storage import PathAndRename
import os


class Upload(BaseModel):
    username = models.CharField(max_length=20, verbose_name=u'上传用户')
    file = models.FileField(upload_to=PathAndRename("./"), blank=True, verbose_name=u'上传文件')
    archive = models.CharField(max_length=201, default=u'其他', null=True, blank=True, verbose_name=u'文件归档')
    filename = models.CharField(max_length=201, null=True, blank=True, verbose_name=u'文件名')
    filepath = models.CharField(max_length=201, null=True, blank=True, verbose_name=u'文件路径')
    type = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'文件类型')
    size = models.CharField(max_length=20, null=True, blank=True, verbose_name=u'文件大小')

    def save(self, *args, **kwargs):
        from re import sub
        self.size = '{}'.format(convert_size(self.file.size))
        filename = os.path.splitext(self.file.name)
        self.filename = '{}-{}{}'.format(sub('\W+', '', filename[0]), self.create_time, filename[1]).replace(' ', '_')
        self.filepath = '{}/{}'.format(self.archive, self.filename)
        super(Upload, self).save(*args, **kwargs)

    def __str__(self):
        return self.filepath

    class Meta:
        verbose_name = u'文件上传'
        verbose_name_plural = u'文件上传'


class FileUpload(models.Model):
    file = models.FileField(upload_to=("./tmp"), blank=True, verbose_name=u'上传文件')

    class Meta:
        verbose_name = u'文件上传'
        verbose_name_plural = u'文件上传'


class RequestEvent(BaseModel):
    url = models.CharField(max_length=255, null=False, db_index=True, verbose_name='请求URI')
    method = models.CharField(max_length=20, null=False, db_index=True, verbose_name='请求方法')
    query_string = models.TextField(verbose_name='请求内容')
    user = models.CharField(max_length=255, null=True, verbose_name='用户')
    remote_ip = models.CharField(max_length=50, null=True, db_index=True, verbose_name='请求IP')

    class Meta:
        ordering = ['-create_time']
        verbose_name = '请求事件'
        verbose_name_plural = verbose_name


class SimpleModel(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
