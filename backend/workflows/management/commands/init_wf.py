# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu


class Command(BaseCommand):
    help = '初始化工作流'

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化工作流菜单 ###########'))
        workflowmenu = Menu.objects.create(name='工作流', code='workflow', curl='/workflow', icon='workflow', sequence=3, type=1,
                                      parent=topmenu)
        menumodel = Menu.objects.create(name='工作流类型', code='wftype', curl='/wftype', icon='wftype', sequence=10, type=2,
                                        parent=workflowmenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='工作流设计', code='wfset', curl='/wfset', icon='wfset', sequence=20, type=2,
                                        parent=workflowmenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='工作流配置', code='wfconf', curl='/wfconf/:id', icon='wfconf', sequence=30, type=2,
                                        hidden=True, active_menu='/wfset', parent=workflowmenu)
        init_menu(menumodel)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
