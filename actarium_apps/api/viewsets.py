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



class UserViewSet( #mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
 
    serializer_class = UserSerializer
    queryset = User.objects.none()
 
    @action(methods=["GET"])
    def mydata(self, request, pk=None):
        if pk and request.user.is_authenticated():
            user = request.user #User.objects.get(id=pk)
            user.organizations = [
                OrganizationsSerializer(ou).data for ou in user.organizationsuser_user.get_orgs_by_role_code("is_member")
            ]
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"status":"error", "message": "inavlid user"},
                            status=status.HTTP_400_BAD_REQUEST)

