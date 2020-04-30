# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from workflows.models import *


class Command(BaseCommand):
    help = '假期工作流'

    def handle(self, *args, **options):
        ## 工作流类型
        type = WorkflowType.objects.get(name='行政', code='ad', order_id=1)

        ## 工作流
        obj = Workflow.objects.get(name='请假单', type=type, ticket_sn_prefix='leave')

        ## 工作流字段
        # 建立内置字段
        CustomField.objects.create(field_name="申请人", order_id=1, field_attribute=True, field_type=10,
                                   field_key="create_user", workflow=obj)
        CustomField.objects.create(field_name="申请时间", order_id=2, field_attribute=True, field_type=40,
                                   field_key="create_time", workflow=obj)
        CustomField.objects.create(field_name="部门", order_id=3, field_attribute=True, field_type=10, field_key="group",
                                   workflow=obj)
        CustomField.objects.create(field_name="工号", order_id=4, field_attribute=True, field_type=10, field_key="id",
                                   workflow=obj)
        # 建立扩展字段
        CustomField.objects.create(field_name="开始时间", order_id=10, field_type=40, field_key="start_time", workflow=obj)
        CustomField.objects.create(field_name="结束时间", order_id=20, field_type=40, field_key="end_time", workflow=obj)

        # 建立初始和结束状态
        State.objects.create(name="开始", order_id=1, state_type=1, is_hidden=True, participant_type=0, participant="",
                             workflow=obj)
        State.objects.create(name="关闭", order_id=99, state_type=2, is_hidden=True, participant_type=0, participant="",
                             workflow=obj)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
