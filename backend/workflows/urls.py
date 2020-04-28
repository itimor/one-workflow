# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url, include
from rest_framework import routers
from workflows.views import WorkflowTypeViewSet, WorkflowViewSet, StateViewSet, TransitionViewSet, CustomFieldViewSet

router = routers.DefaultRouter()

router.register(r'workflowtype', WorkflowTypeViewSet)
router.register(r'workflow', WorkflowViewSet)
router.register('state', StateViewSet)
router.register(r'transition', TransitionViewSet)
router.register(r'customfield', CustomFieldViewSet)


urlpatterns = [
]

urlpatterns += router.urls
