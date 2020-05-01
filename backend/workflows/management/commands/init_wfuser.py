# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = '初始化 工单所需 角色 用户 分组'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('############ 初始化分组 ###########'))
        topgroup = Group.objects.get(name='top', code='top')

        group_ops = Group.objects.create(name='运维', code='ops', sequence=1, parent=topgroup)
        group_dev = Group.objects.create(name='开发', code='dev', sequence=2, parent=topgroup)
        group_hr = Group.objects.create(name='人事', code='hr', sequence=3, parent=topgroup)

        self.stdout.write(self.style.SUCCESS('############ 初始化角色 ###########'))
        toprole = Role.objects.get(name='top', code='top')

        role_ops_tl = Role.objects.create(name='运维经理', code='ops_tl', sequence=1, group=group_ops, parent=toprole)
        role_ops = Role.objects.create(name='运维', code='ops', sequence=1, group=group_ops, parent=role_ops_tl)
        role_dev_tl = Role.objects.create(name='开发经理', code='dev_tl', sequence=2, group=group_dev, parent=toprole)
        role_dev = Role.objects.create(name='开发', code='dev', sequence=2, group=group_dev, parent=role_dev_tl)
        role_hr_tl = Role.objects.create(name='人事经理', code='hr_tl', sequence=3, group=group_hr, parent=toprole)
        role_hr = Role.objects.create(name='人事', code='hr', sequence=3, group=group_hr, parent=role_hr_tl)

        self.stdout.write(self.style.SUCCESS('############ 初始化用户 ###########'))
        ops_tl = User.objects.create(username='ops_tl', password=make_password("123456"), group=group_ops)
        ops_tl.roles.add(role_ops_tl)
        ops = User.objects.create(username='ops', password=make_password("123456"), group=group_ops)
        ops.roles.add(role_ops)
        dev_tl = User.objects.create(username='dev_tl', password=make_password("123456"), group=group_dev)
        dev_tl.roles.add(role_dev_tl)
        dev = User.objects.create(username='dev', password=make_password("123456"), group=group_dev)
        dev.roles.add(role_dev)
        hr_tl = User.objects.create(username='hr_tl', password=make_password("123456"), group=group_hr)
        hr_tl.roles.add(role_hr_tl)
        hr = User.objects.create(username='hr', password=make_password("123456"), group=group_hr)
        hr.roles.add(role_hr)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
