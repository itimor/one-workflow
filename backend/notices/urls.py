# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from notices.views import NoticeViewSet, MailBotViewSet, TelegramBotViewSet

router = routers.DefaultRouter()

router.register(r'notice', NoticeViewSet)
router.register(r'mail', MailBotViewSet)
router.register(r'telegram', TelegramBotViewSet)

urlpatterns = [
]

urlpatterns += router.urls
