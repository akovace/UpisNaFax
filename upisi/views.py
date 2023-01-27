from rest_framework.permissions import IsAuthenticated
from django.views.generic.base import TemplateView
#from rest_flex_fields import FlexFieldsModelViewSet
from .serializers import UserAdminSerializer, RegistracijaSerializer, UserSerializer, GroupSerializer, PrijavnicaSerializer,VrstaSmjeraSerializer, PredmetiSerializer, LOG_upisaSerializer
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

# Registracija http://localhost:8000/registracija/

class Registracija(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(pk = request.user.id)
            if user.groups.filter(name = 'administrator').exists():
                group = request.data.get('groups')
            else:
                group = [2]
        else:
            group = [2]

        data = {
            'username': request.data.get('username'), 
            'password': request.data.get('password'), 
            'email': request.data.get('email'),
            'groups': group

        }

        serializer = RegistracijaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Prijavnica http://localhost:8000/prijavnica/

class PrijavnicaZaUpis(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = request.user.id)
        if user.groups.filter(name = 'administrator').exists():
            prijavnica = Prijavnica.objects.all()
        else:
            prijavnica = Prijavnica.objects.filter(student = user)
        
        serializers = PrijavnicaSerializer(prijavnica, many=True)  
        return Response(serializers.data, status=200)

    def post(self, request, *args, **kwargs):

        user = User.objects.get(pk = request.user.id)
        if user.groups.filter(name = 'administrator').exists():
            student = request.data.get('student')
        else:
            student = request.user.id

        data = {
                'student': student, 
                'datum_rodjenja': request.data.get('datum_rodjenja'), 
                'mjesto_rodjenja': request.data.get('mjesto_rodjenja'), 
                'zavrsena_skola': request.data.get('zavrsena_skola'), 
                'molba_za_upis_na_smjer': request.data.get('molba_za_upis_na_smjer'), 
                'odabir_smjera': request.data.get('odabir_smjera'), 
                'dokument_o_zavrsenoj_skoli': request.data.get('dokument_o_zavrsenoj_skoli'), 
                'prosjek_ocjena': request.data.get('prosjek_ocjena'), 
                'ocjena_na_maturi': request.data.get('ocjena_na_maturi'), 
                'status': '0', 
                'datum_kriranja': request.data.get('datum_kriranja')
        }

        smjer = VrstaSmjera.objects.get(pk = request.data.get('odabir_smjera'))

        prijavnica = Prijavnica.objects.filter(student = request.user.id, odabir_smjera = request.data.get('odabir_smjera'))
        if prijavnica:
            return Response({"message": "prijava za smjer " + smjer.naziv_smjera + " vec postoji"}, status=status.HTTP_400_BAD_REQUEST)

        broj_prijava = Prijavnica.objects.filter(odabir_smjera = request.data.get('odabir_smjera'), status = '1')

        if broj_prijava.count() > smjer.kvota:
            return Response({"message": "kvota za smjer " + smjer.naziv_smjera + " je popunjena"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PrijavnicaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        permission_classes = [permissions.IsAuthenticated]


# Smjer i pregled predmeta http://localhost:8000/vrstasmjera/

class VrstaSmjeraPregled(viewsets.ModelViewSet):

    serializer_class = VrstaSmjeraSerializer
    queryset = VrstaSmjera.objects.all()
    permission_classes = [IsAuthenticated]


#Pregled studenata i njihovih prijava http://localhost:8000/studentiprijave/
class StudentiPrijave(APIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = request.user.id)
        if user.groups.filter(name = 'administrator').exists():
            queryset = User.objects.filter(groups = 2)
        else:
            queryset = User.objects.filter(id = user.id)
        #queryset = User.objects.all()
        serializers = UserAdminSerializer(queryset, many=True)  
        return Response(serializers.data, status=200)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAuthenticated]


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



class Predmeti(viewsets.ModelViewSet):

    serializer_class = PredmetiSerializer
    queryset = Predmeti.objects.all()
    permission_classes = [IsAuthenticated]

class LOG_upisa(viewsets.ModelViewSet):

    serializer_class = LOG_upisaSerializer
    queryset = LOG_upisa.objects.all()
    permission_classes = [IsAuthenticated]