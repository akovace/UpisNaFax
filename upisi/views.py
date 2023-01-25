from rest_framework.permissions import IsAuthenticated
from django.views.generic.base import TemplateView
#from rest_flex_fields import FlexFieldsModelViewSet
from .serializers import UserSerializer, GroupSerializer, PrijavnicaSerializer,VrstaSmjeraSerializer, PredmetiSerializer, LOG_upisaSerializer
from upisi.models import Prijavnica, Predmeti, LOG_upisa, VrstaSmjera
from rest_framework import generics, viewsets, permissions
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission, User
from django.shortcuts import render
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status

# Registracija http://localhost:8000/users/
class UserListApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = {
            'username': request.data.get('username'), 
            'password': request.data.get('password'), 
            'email': request.data.get('email'),
            'group': 'student'

        }
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrijavnicaPregled(viewsets.ModelViewSet):

    serializer_class = PrijavnicaSerializer
    queryset = Prijavnica.objects.all()
    permission_classes = [IsAuthenticated]

class VrstaSmjera(viewsets.ModelViewSet):

    serializer_class = VrstaSmjeraSerializer
    user = User.objects.get(pk = 1)
    if user.groups.filter(name='administrator').exists():
        queryset = VrstaSmjera.objects.all()
    else:
        queryset = VrstaSmjera.objects.filter(id = 1)
    permission_classes = [IsAuthenticated]

class Predmeti(viewsets.ModelViewSet):

    serializer_class = PredmetiSerializer
    queryset = Predmeti.objects.all()
    permission_classes = [IsAuthenticated]

class LOG_upisa(viewsets.ModelViewSet):

    serializer_class = LOG_upisaSerializer
    queryset = LOG_upisa.objects.all()
    permission_classes = [IsAuthenticated]