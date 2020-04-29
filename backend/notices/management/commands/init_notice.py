# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu


class Command(BaseCommand):
    help = '初始化工作流'

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化通知菜单 ###########'))
        noticemenu = Menu.objects.create(name='通知管理', code='notice', curl='/notice', icon='notice', sequence=5, type=1,
                                         parent_id=topmenu.id)
        menumodel = Menu.objects.create(name='mail通知', code='mail', curl='/mail', icon='mail', sequence=10, type=2,
                                        parent_id=noticemenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='telegram通知', code='telegram', curl='/telegram', icon='telegram',
                                        sequence=20, type=2, parent_id=noticemenu.id)
        init_menu(menumodel)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
