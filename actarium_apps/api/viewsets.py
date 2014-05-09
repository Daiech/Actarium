# -*- coding:utf-8 -*-

# import models
from django.contrib.auth.models import User
from actarium_apps.organizations.models import Organizations
from actarium_apps.organizations.models import OrganizationsUser

# import rest_framework elements
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# import custom elements
from .serializers import UserSerializer
from .serializers import OrganizationsSerializer
from .serializers import GroupsSerializer


class UserViewSet( #mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
 
    serializer_class = UserSerializer
    queryset = User.objects.none()
 
    @action(methods=["GET"])
    def mydata(self, request, pk=None):
        if pk and request.user.is_authenticated():
            user = request.user
            orgs = [ou for ou in user.organizationsuser_user.get_orgs_by_role_code("is_member")]
            user.organizations = []
            for org in orgs:
                group_list = org.get_groups() if org.has_user_role(user, "is_admin") else org.get_my_groups(user)
                org.groups = [GroupsSerializer(gr).data for gr in group_list]
                user.organizations.append(OrganizationsSerializer(org).data)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"status":"error", "message": "inavlid user"},
                            status=status.HTTP_400_BAD_REQUEST)

