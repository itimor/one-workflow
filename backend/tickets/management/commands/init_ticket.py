# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu


class Command(BaseCommand):
    help = '初始化工作流'

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化工单菜单 ###########'))
        ticketmenu = Menu.objects.create(name='工单系统', code='ticket', curl='/ticket', icon='ticket', sequence=4, type=1,
                                      parent_id=topmenu.id)
        menumodel = Menu.objects.create(name='新建工单', code='new_ticket', curl='/new_ticket', icon='new_ticket', sequence=10, type=2,
                                        parent_id=ticketmenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='编辑工单', code='u_ticket', curl='/u_ticket/:id', icon='u_ticket', sequence=10, type=2,
                                        hidden=True, active_menu='/new_ticket', parent_id=ticketmenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='处理工单', code='s_ticket', curl='/s_ticket/:id', icon='s_ticket', sequence=10, type=2,
                                        hidden=True, active_menu='/todo_ticket', parent_id=ticketmenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='我的工单', code='my_ticket', curl='/my_ticket', icon='my_ticket', sequence=30, type=2,
                                        no_cache=True, parent_id=ticketmenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='我的待办', code='todo_ticket', curl='/todo_ticket', icon='todo_ticket', sequence=40, type=2,
                                        no_cache=True, parent_id=ticketmenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='所有工单', code='all_ticket', curl='/all_ticket', icon='all_ticket', sequence=90, type=2,
                                        no_cache=True, parent_id=ticketmenu.id)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='查看工单', code='c_ticket', curl='/c_ticket/:id', icon='list', sequence=100, type=2,
                                        hidden=True, active_menu='/my_ticket', parent_id=ticketmenu.id)
        init_menu(menumodel)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
