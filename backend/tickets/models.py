# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel
from workflows.models import *

participant_type = (
    (0, '无处理人'),
    (1, '个人'),
    (2, '多人'),
    (3, '部门'),
    (4, '角色'),
)

act_state = (
    (0, '草稿中'),
    (1, '进行中'),
    (2, '被退回'),
    (3, '被撤回'),
    (4, '已完成'),
    (5, '已关闭'),
)


class Ticket(BaseModel):
    """
    工单记录
    """
    name = models.CharField(u'标题', max_length=112, blank=True, default='', help_text="工单的标题")
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    sn = models.CharField(u'流水号', max_length=25, help_text="工单的流水号")
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='当前状态')
    participant_type = models.CharField(max_length=1, choices=participant_type, default=0, verbose_name='当前处理人类型')
    participant = models.CharField('当前处理人', max_length=100, default='', blank=True,
                                   help_text='可以为空(无处理人的情况，如结束状态)、username\多个username(以,隔开)\部门id\角色id\脚本文件名等')
    relation = models.CharField('工单关联人', max_length=255, default='', blank=True,
                                help_text='工单流转过程中将保存所有相关的人(包括创建人、曾经的待处理人)，用于查询')
    act_state = models.CharField(max_length=1, choices=act_state, default=0, verbose_name='进行状态')
    multi_all_person = models.TextField('全部处理的结果', default='{}', help_text='需要当前状态处理人全部处理时实际的处理结果，json格式')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工单记录'
        verbose_name_plural = verbose_name


intervene_type = (
    (0, '转交操作'),
    (1, '接单操作'),
    (2, '评论操作'),
    (3, '删除操作'),
    (4, '强制关闭操作'),
    (5, '强制修改状态操作'),
    (6, '撤回'),
)


class TicketFlowLog(BaseModel):
    """
    工单流转日志
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='工单')
    transition = models.ForeignKey(Transition, on_delete=models.CASCADE, verbose_name='流转')
    suggestion = models.TextField('处理意见', default='', blank=True)
    participant_type = models.CharField(max_length=1, choices=participant_type, default=0, verbose_name='处理人类型')
    participant = models.CharField('处理人', max_length=50, default='', blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='当前状态')
    intervene_type = models.CharField(max_length=1, choices=intervene_type, default=0, verbose_name='干预类型')
    ticket_data = models.TextField('工单数据', default='', blank=True, help_text='可以用于记录当前表单数据，json格式')

    class Meta:
        verbose_name = '工单流转日志'
        verbose_name_plural = verbose_name


field_type = (
    (5, '字符串'),
    (10, '整形'),
    (15, '浮点型'),
    (20, '布尔'),
    (25, '日期'),
    (30, '时间'),
    (35, '日期时间'),
    (40, '单选框'),
    (45, '多选框'),
    (50, '下拉列表'),
    (55, '多选下拉列表'),
    (60, '文本域'),
    (65, '用户名'),
    (70, '多选的用户名'),
)


class TicketCustomField(BaseModel):
    """
    工单自定义字段， 工单自定义字段实际的值。
    """
    name = models.CharField(u'字段名', max_length=50)
    field_key = models.CharField(u'字段标识', max_length=50)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='工单')
    field_type = models.CharField(max_length=1, choices=field_type, default=0, verbose_name='字段类型')
    char_value = models.CharField('字符串值', max_length=255, default='', blank=True)
    int_value = models.IntegerField('整形值', default=0, blank=True)
    float_value = models.FloatField('浮点值', default=0.0, blank=True)
    bool_value = models.BooleanField('布尔值', default=False, blank=True)
    # date_value = models.DateField('日期值', default='0001-01-01', blank=True)
    date_value = models.DateField('日期值', auto_now_add=True, blank=True)
    # datetime_value = models.DateTimeField('日期时间值', default='0001-01-01 00:00:00', blank=True)
    datetime_value = models.DateTimeField('日期时间值', auto_now_add=True, blank=True)
    # time_value = models.TimeField('时间值', default='00:00:01', blank=True)
    time_value = models.TimeField('时间值', auto_now_add=True, blank=True)
    radio_value = models.CharField('radio值', default='', max_length=50, blank=True)
    checkbox_value = models.CharField('checkbox值', default='', max_length=50, blank=True, help_text='逗号隔开多个选项')
    select_value = models.CharField('下拉列表值', default='', max_length=50, blank=True)
    multi_select_value = models.CharField('多选下拉列表值', default='', max_length=50, blank=True, help_text='逗号隔开多个选项')
    text_value = models.TextField('文本值', default='', blank=True)
    username_value = models.CharField('用户名', max_length=50, default='', blank=True)
    multi_username_value = models.CharField('多选用户名', max_length=255, default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工单自定义字段'
        verbose_name_plural = verbose_name


class TicketUser(BaseModel):
    """
    工单关系人, 用于加速待办工单及关联工单列表查询
    """
    ticket = models.ForeignKey(Ticket, null=True, blank=True, on_delete=models.SET_NULL)
    username = models.CharField('关系人', max_length=100)
    in_process = models.BooleanField('待处理中', default=False)
    worked = models.BooleanField('处理过', default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '工单关系人'
        verbose_name_plural = verbose_name
