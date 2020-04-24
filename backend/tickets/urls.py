# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url, include
from rest_framework import routers
from tickets.views import TicketViewSet, TicketFlowLogViewSet, TicketCustomFieldViewSet, TicketUserViewSet

router = routers.DefaultRouter()

router.register(r'tickiet', TicketViewSet)
router.register('ticketflowlog', TicketFlowLogViewSet)
router.register(r'ticketcustomfield', TicketCustomFieldViewSet)
router.register(r'ticketuser', TicketUserViewSet)

urlpatterns = [
]

urlpatterns += router.urls
