# -*- coding:utf-8 -*-

# import models
from django.contrib.auth.models import User
from actarium_apps.organizations.models import Organizations
from actarium_apps.organizations.models import Groups

# import rest_framework elements
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User class"""

    organizations = serializers.RelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'organizations')


class OrganizationsSerializer(serializers.ModelSerializer):
    """Serializer for Organizations class"""
    
    groups = serializers.RelatedField(many=True)

    class Meta:
        model = Organizations
        fields = ('id', 'name', 'slug', 'description', 'image_path','groups',)


class GroupsSerializer(serializers.ModelSerializer):
    """Serializer for Groups class"""
    
    class Meta:
        model = Groups
        fields = ('id', 'name','description','image_path',)






