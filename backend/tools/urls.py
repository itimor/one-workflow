# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from tools.views import UploadViewSet, FileUploadViewSet, RequestEventViewSet, SimpleViewSet

router = routers.DefaultRouter()

router.register(r'upload', UploadViewSet)
router.register(r'fileupload', FileUploadViewSet)
router.register(r'auditlog', RequestEventViewSet)
router.register('simple', SimpleViewSet)

urlpatterns = [
]

urlpatterns += router.urls
