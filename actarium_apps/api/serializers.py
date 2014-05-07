# -*- coding:utf-8 -*-

# import models
from django.contrib.auth.models import User
from actarium_apps.organizations.models import Organizations

# import rest_framework elements
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User class"""

    organizaciones = serializers.RelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email','organizaciones')


class OrganizationsSerializer(serializers.ModelSerializer):
    """Serializer for Organizations class"""

    class Meta:
        model = Organizations
        fields = ('id', 'name', 'slug', 'description', 'image_path',)






