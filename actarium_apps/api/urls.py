# -*- coding:utf-8 -*-

# import django elements
from django.conf.urls import patterns, include, url

# import rest_framework elements
from rest_framework.routers import DefaultRouter

# import custom elements
from .viewsets import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)


name = "rest"
namespace = 'rest_framework'

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
)


