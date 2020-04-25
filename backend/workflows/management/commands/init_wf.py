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
                                      parent_id=topmenu.id)
        menumodel = Menu.objects.create(name='工作流设计', code='wfset', curl='/wfset', icon='wfset', sequence=10, type=2,
                                        parent_id=workflowmenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='工作流配置', code='wfconf', curl='/wfconf', icon='wfconf', sequence=20, type=2,
                                        parent_id=workflowmenu.id)
        init_menu(menumodel)
        # menumodel = Menu.objects.create(name='我相关的', code='myticket', curl='/myticket', icon='myticket', sequence=20, type=2,
        #                                 parent_id=wfmanagermenu.id)
        # init_menu(menumodel)
        # menumodel = Menu.objects.create(name='所有工单', code='myticket', curl='/myticket', icon='myticket', sequence=20, type=2,
        #                                 parent_id=wfmanagermenu.id)
        # init_menu(menumodel)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
