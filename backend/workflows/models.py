# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel
from systems.models import *


class WorkflowType(BaseModel):
    name = models.CharField('名称', max_length=50)
    status = models.BooleanField(default=True)
    code = models.CharField(max_length=32, unique=True, verbose_name='代码')
    order_id = models.IntegerField('状态顺序', default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order_id']
        verbose_name = '工作流类型'
        verbose_name_plural = verbose_name


class Workflow(BaseModel):
    """
    工作流
    """
    name = models.CharField('名称', max_length=50)
    ticket_sn_prefix = models.CharField('工单流水号前缀', default='xxoo', max_length=20)
    status = models.BooleanField(default=True)
    type = models.ForeignKey(WorkflowType, on_delete=models.CASCADE, verbose_name='工作流类型')
    view_permission_check = models.BooleanField('查看权限校验', default=True, help_text='开启后，只允许工单的关联人(创建人、曾经的处理人)有权限查看工单')
    limit_expression = models.TextField('限制表达式', default='{}', blank=True,
                                        help_text='限制周期({"period":24} 24小时), 限制次数({"count":1}在限制周期内只允许提交1次), 限制级别({"level":1} 针对(1单个用户 2全局)限制周期限制次数,默认特定用户);允许特定人员提交({"allow_persons":"zhangsan,lisi"}只允许张三提交工单,{"allow_depts":"1,2"}只允许部门id为1和2的用户提交工单，{"allow_roles":"1,2"}只允许角色id为1和2的用户提交工单)')
    display_form_str = models.TextField('展现表单字段', default='[]', blank=True,
                                        help_text='默认"[]"，用于用户只有对应工单查看权限时显示哪些字段,field_key的list的json,如["days","sn"],内置特殊字段participant_info.participant_name:当前处理人信息(部门名称、角色名称)，state.state_name:当前状态的状态名,workflow.workflow_name:工作流名称')
    title_template = models.CharField('标题模板', max_length=50, default='你有一个待办工单:{title}', null=True, blank=True,
                                      help_text='工单字段的值可以作为参数写到模板中，格式如：你有一个待办工单:{title}')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工作流'
        verbose_name_plural = verbose_name


field_type = {
    1: '字符串',
    2: '整型',
    3: '浮点型',
    4: '布尔',
    5: '日期',
    6: '日期时间',
    7: '范围日期',
    8: '文本域',
    9: '单选框',
    10: '下拉列表',
    11: '用户名',
    12: '多选框',
    13: '多选下拉',
    14: '多选用户名',
}


class CustomField(BaseModel):
    """自定义字段, 设定某个工作流有哪些自定义字段"""
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    field_attribute = models.BooleanField('字段是否内置', default=False)
    field_type = models.CharField(max_length=1, choices=tuple(field_type.items()), default=0, verbose_name='字段类型')
    field_key = models.CharField('字段标识', max_length=50, help_text='字段类型请尽量特殊，避免与系统中关键字冲突')
    field_name = models.CharField('字段名称', max_length=50)
    # 内置 field 的 order_id 不要超过10
    order_id = models.IntegerField('排序', default=0)
    default_value = models.CharField('默认值', null=True, blank=True, max_length=100, help_text='前端展示时，可以将此内容作为表单中的该字段的默认值')
    field_template = models.TextField('文本域模板', default='', blank=True, help_text='文本域类型字段前端显示时可以将此内容作为字段的placeholder')
    boolean_field_display = models.CharField('布尔类型显示名', max_length=100, default='{}', blank=True,
                                             help_text='当为布尔类型时候，可以支持自定义显示形式。{"1":"是","0":"否"}或{"1":"需要","0":"不需要"}，注意数字也需要引号')
    field_choice = models.CharField('radio、checkbox、select的选项', max_length=255, default='{}', blank=True,
                                    help_text='radio,checkbox,select,multiselect类型可供选择的选项，格式为json如:{"1":"中国", "2":"美国"},注意数字也需要引号')
    label = models.CharField('标签', max_length=100, blank=True, default='{}',
                             help_text='自定义标签，json格式，调用方可根据标签自行处理特殊场景逻辑，loonflow只保存文本内容')

    def __str__(self):
        return self.field_name

    class Meta:
        ordering = ['order_id']
        verbose_name = '工作流自定义字段'
        verbose_name_plural = verbose_name


# 0.普通类型 1.初始状态(用于新建工单时,获取对应的字段必填及transition信息) 2.结束状态(此状态下的工单不得再处理，即没有对应的transition)
state_type = {
    0: '普通状态',
    1: '初始状态',
    2: '结束状态',
}

participant_type = {
    0: '无处理人',
    1: '个人',
    2: '部门',
    3: '角色',
}


class State(BaseModel):
    """
    状态记录, 变量支持通过脚本获取
    """
    name = models.CharField('名称', max_length=50)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    is_hidden = models.BooleanField('是否隐藏', default=False, help_text='设置为True时,获取工单步骤api中不显示此状态(当前处于此状态时除外)')
    order_id = models.IntegerField('状态顺序', default=1)
    state_type = models.CharField(max_length=1, choices=tuple(state_type.items()), default=0, verbose_name='状态类型')
    enable_retreat = models.BooleanField('允许撤回', default=False, help_text='开启后允许工单创建人在此状态直接撤回工单到初始状态')
    participant_type = models.CharField(max_length=1, choices=tuple(participant_type.items()), default=0, verbose_name='参与者类型')
    user_participant = models.ManyToManyField(User, blank=True, verbose_name='参与用户')
    group_participant = models.ManyToManyField(Group, blank=True, verbose_name='参与组')
    role_participant = models.ManyToManyField(Role, blank=True, verbose_name='参与角色')
    fields = models.ManyToManyField(CustomField, blank=True, verbose_name='可编辑字段')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order_id']
        verbose_name = '工作流状态'
        verbose_name_plural = verbose_name


transition_name = {
    0: '保存',
    1: '通过',
    2: '驳回',
    3: '撤销',
    4: '关闭',
}

transition_type = {
    0: '常规流转',
    1: '定时器流转',
}

attribute_type = {
    0: '草稿中',
    1: '进行中',
    2: '被退回',
    3: '被撤销',
    4: '已完成',
    5: '已关闭',
}


class Transition(BaseModel):
    """
    工作流流转，定时器，条件(允许跳过)， 条件流转与定时器不可同时存在
    """
    name = models.CharField('名称类型', max_length=1, choices=tuple(transition_name.items()), default=1)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='工作流')
    transition_type = models.CharField('流转类型', max_length=1, choices=tuple(transition_type.items()), default=0)
    timer = models.IntegerField('定时器(单位秒)', default=0, help_text='流转类型设置为定时器流转时生效,单位秒。处于源状态X秒后如果状态都没有过变化则自动流转到目标状态')
    source_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL, related_name="source_state", verbose_name='源状态')
    dest_state = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL, related_name="dest_state", verbose_name='目的状态')
    condition_expression = models.TextField('条件表达式', default='[]',
                                            help_text='流转条件表达式，根据表达式中的条件来确定流转的下个状态，格式为[{"expression":"{days} > 3 and {days}<10", "target_state_id":11}] 其中{}用于填充工单的字段key,运算时会换算成实际的值，当符合条件下个状态将变为target_state_id中的值,表达式只支持简单的运算或datetime/time运算.loonflow会以首次匹配成功的条件为准，所以多个条件不要有冲突')
    attribute_type = models.CharField(max_length=1, choices=tuple(attribute_type.items()), default=0, verbose_name='属性类型')
    alert_enable = models.BooleanField('点击弹窗提示', default=False)
    alert_text = models.CharField('弹窗内容', max_length=100, default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工作流流转'
        verbose_name_plural = verbose_name
