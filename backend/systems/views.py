# -*- coding: utf-8 -*-
# author: timor

from systems.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin
from rest_framework.decorators import action
from systems.menus import get_menus_by_user, set_menu
from common import status
from collections import OrderedDict
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView, jwt_response_payload_handler
from rest_framework_jwt.settings import api_settings
from datetime import datetime


class UserViewSet(BulkModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username']
    filter_fields = ['username']
    ordering_fields = ['username', 'status']


class GroupViewSet(BulkModelMixin):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']


class RoleViewSet(BulkModelMixin):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['name']


class MenuViewSet(BulkModelMixin):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']


class AuthViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], url_path='getuserinfo', detail=False)
    def getuserinfo(self, request):
        user = request.user
        user_obj = User.objects.get(username=user)

        data = get_menus_by_user(user)

        if len(data) > 0:
            topmenuid = data[0].parent_id
            if not topmenuid:
                topmenuid = data[0].id

        menus = set_menu(data, topmenuid)

        ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if not ip:
            ip = request.META.get('REMOTE_ADDR', "")

        data = {'menus': menus, 'username': user_obj.username, 'avatar': user_obj.avatar, 'memo': user_obj.memo,
                'ip': ip}
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))

    @action(methods=['get'], url_path='getmenubutons', detail=False)
    def getmenubutons(self, request):
        user = request.user
        user_obj = User.objects.get(username=user)
        buttons = []

        if user_obj.is_admin:
            buttons = ['add', 'del', 'update', 'view']
        else:
            menucode = request.GET['menucode']

            match_menu = Menu.objects.get(code=menucode)

            data = get_menus_by_user(user)
            for item in data:
                if item.parent_id == match_menu.id:
                    buttons.append(item.operate)
        data = buttons
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))


class ObtainJSONWebToken(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = JsonResponse(OrderedDict([
                ('results', response_data)
            ], code=status.HTTP_200_OK))
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        return JsonResponse(OrderedDict([
            ('results', serializer.errors)
        ], code=status.HTTP_500_INTERNAL_SERVER_ERROR))
