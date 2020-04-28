# -*- coding: utf-8 -*-
# author: itimor

from systems.models import *
from itertools import chain


# 获取管理员权限下所有菜单
def get_menus_by_user(user):
    user_obj = User.objects.get(username=user)

    if user_obj.is_admin:
        menus = Menu.objects.all()
    else:
        user_roles = user_obj.roles.all()
        group_roles = user_obj.group.roles.all()
        all_roles = sorted(chain(user_roles, group_roles), key=lambda t: t.id, reverse=True)
        print("用户拥有角色: %s" % all_roles)

        menu_list = [item.menus.all() for item in all_roles if item.menus.all()][0]

        menuMap = dict()
        for item in menu_list:
            menuMap[item.id] = item
        for item in menu_list:
            if item.parent_id in menuMap:
                continue
            user_menus = find_menu_daddy(item.parent_id, menuMap)
        menus = [user_menus[i] for i in sorted(user_menus.keys())]
    return menus


def find_menu_daddy(menuid, menuMap):
    obj = Menu.objects.filter(id=menuid).first()
    if obj:
        mid = obj.id
        if mid not in menuMap:
            menuMap[mid] = obj
            find_menu_daddy(obj.parent_id, menuMap)
            return menuMap


def set_menu(menus, parent_id):
    amenus = [i for i in menus if i.parent_id == parent_id]

    if len(amenus) == 0:
        return []

    all_menus = []
    for item in amenus:
        menu = {
            'path': item.curl,
            'component': item.code,
            'name': item.code,
            'hidden': item.hidden,
            'meta': {'title': item.code, 'icon': item.icon, 'no_cache': item.no_cache, 'active_menu': item.active_menu,
                     'hidden': item.hidden,
                     },
            'children': []
        }
        if item.type == 3:
            menu['hidden'] = True

        # 查询是否有子级
        menu_children = set_menu(menus, item.id)
        if len(menu_children) > 0:
            menu['children'] = menu_children

        if item.type == 2:
            # 添加子级首页，有这一级NoCache才有效
            menu_index = {
                'path': 'index',
                'component': item.code,
                'name': item.code,
                'hidden': item.hidden,
                'meta': {'title': item.code, 'icon': item.icon, 'no_cache': item.no_cache,
                         'active_menu': item.active_menu, 'hidden': item.hidden,
                         },
                'children': []
            }
            menu['children'].append(menu_index)
            menu['meta'] = []

        all_menus.append(menu)
    return all_menus


# 新增菜单后自动添加菜单下的常规操作
def init_menu(menu):
    if menu.type == 2:
        menu_list = [
            {"name": "新增", "code": menu.code + "add", "curl": menu.curl + "/add", 'type': 3, "operate": "add",
             "sequence": 10},
            {"name": "删除", "code": menu.code + "del", "curl": menu.curl + "/del", 'type': 3, "operate": "del",
             "sequence": 20},
            {"name": "编辑", "code": menu.code + "update", "curl": menu.curl + "/update", 'type': 3, "operate": "update",
             "sequence": 30},
            {"name": "查看", "code": menu.code + "view", "curl": menu.curl + "/view", 'type': 3, "operate": "view",
             "sequence": 40},
        ]

        menu_models = []
        for item in menu_list:
            menu_models.append(Menu(name=item['name'], code=item['code'], curl=item['curl'], type=item['type'],
                                    operate=item['operate'],
                                    sequence=item['sequence'], parent_id=menu.id, hidden=True))
        Menu.objects.bulk_create(menu_models)
