# -*- coding: utf-8 -*-
# author: itimor

from django_filters import rest_framework as filters
from tickets.models import *


class TicketFilter(filters.FilterSet):
    class Meta:
        model = Ticket

        fields = {
            'id': ['exact'],
            'name': ['exact'],
            'participant': ['exact'],
            'create_user__username': ['exact'],
            "transition__attribute_type": ["lt"],
        }
