# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url, include
from rest_framework import routers
from rest_auth.views import PasswordChangeView
from systems.views import UserViewSet, GroupViewSet, RoleViewSet, PermissionViewSet, MenuViewSet, AuthViewSet, \
    ObtainJSONWebToken

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'group', GroupViewSet)
router.register(r'role', RoleViewSet)
router.register(r'perm', PermissionViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'auth', AuthViewSet)

urlpatterns = [
    url(r'^auth/changepwd/', PasswordChangeView.as_view(), name='changepwd'),
    # token认证
    url(r'^auth/jwt-token-auth/', ObtainJSONWebToken.as_view(), name='rest_framework_token'),
    url(r'^auth/api-token-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls
