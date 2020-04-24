# -*- coding: utf-8 -*-
# author: itimor


from rest_framework.permissions import BasePermission
from systems.models import *
from itertools import chain

parse_method_action = {
    'GET': 'view',
    'POST': 'add',
    'PUT': 'change',
    'PATCH': 'change',
    'DELETE': 'delete',
}

ignore_path = [
    '/api/sys/auth/jwt-token-auth/',
    '/api/sys/auth/getuserinfo/',
    '/api/sys/auth/getmenubutons/',
]


def check_permission(request, perm):
    user = User.objects.get(username=request.user)

    if user.is_admin:
        return True

    if request.path in ignore_path:
        return True

    user_roles = user.roles.all()
    group_roles = user.group.roles.all()

    all_roles = sorted(chain(user_roles, group_roles), key=lambda t: t.id, reverse=True)
    perms = Permission.objects.filter(role__in=all_roles)
    for i in perms:
        if i.codename == perm:
            return True


class IsOwnerRoles(BasePermission):

    def has_permission(self, request, view):
        app = view.get_view_name().split()[0].lower()
        perm = 'view_' + app
        return check_permission(request, perm)

    def has_object_permission(self, request, view, obj):
        app_label = obj._meta.app_label
        model = obj._meta.object_name.lower()
        perm = '{}_{}'.format(parse_method_action[request.method], model)
        return check_permission(request, perm)
