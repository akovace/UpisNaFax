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
from datetime import datetime

# Registracija, nije potrabna autentifikacija http://localhost:8000/registracija/

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

# Administratori mogu brisati korisnike DELETE http://localhost:8000/korisnik/16/

class Korisnik(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    #def get(self, request, *args, **kwargs):
    #    queryset = User.objects.all()
    #    serializers = UsersSerializer(queryset, many=True)  
    #    return Response(serializers.data, status=200)

    def delete(self, request, user_id, *args, **kwargs):
        prijavljeniuser = User.objects.get(pk = request.user.id)
        if prijavljeniuser.groups.filter(name = 'administrator').exists():
            user = self.get_object(user_id)
            if not user:
                return Response(
                    {"res": "Object with user id does not exists"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                user.delete()
            return Response(
                {"res": "Object deleted!"},
                status=status.HTTP_200_OK
                )
        else:
            return Response(
                {"res": "Nisi administrator"},
                status=status.HTTP_200_OK
                )

# Prijavnica GET i POST http://localhost:8000/prijavnica/

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
#Unutar svakog smjera su vidljivi predmeti i injihovi opisi

class VrstaSmjeraPregled(viewsets.ModelViewSet):

    serializer_class = VrstaSmjeraSerializer
    queryset = VrstaSmjera.objects.all()
    permission_classes = [IsAuthenticated]


#Pregled studenata i njihovih prijava http://localhost:8000/studentiprijave/
class StudentiPrijave(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = request.user.id)
        if user.groups.filter(name = 'administrator').exists():
            queryset = User.objects.filter(groups = 2)
        else:
            queryset = User.objects.filter(id = user.id)
        #queryset = User.objects.all()
        serializers = UserAdminSerializer(queryset, many=True)  
        return Response(serializers.data, status=200)

# GET i POST http://localhost:8000/odobrenje/

class Odobrenja(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = request.user.id)
        if user.groups.filter(name = 'administrator').exists():
            logupisa = LOG_upisa.objects.all()        
            serializers = LOG_upisaSerializer(logupisa, many=True)  
            return Response(serializers.data, status=200)
        else:
            return Response(
                {"res": "Nisi administrator"},
                status=status.HTTP_200_OK
                )

    def post(self, request, *args, **kwargs):

        user = User.objects.get(pk = request.user.id)
        if user.groups.filter(name = 'administrator').exists():

            provjeraLOGa = LOG_upisa.objects.filter(administrator = user.id, prijavnica = request.data.get('prijavnica'))
            if provjeraLOGa.count() > 0:
                return Response(
                {"res": "zahtjev je vec obradjen"},
                status=status.HTTP_200_OK
                )


            data = {
                'administrator': user.id, 
                'prijavnica': request.data.get('prijavnica'), 
                'opis_odobrenja': request.data.get('opis_odobrenja'), 
                'status': request.data.get('status'), 
                'vrijeme_odobrenja': datetime.now()
            }


            serializer = LOG_upisaSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                updateprijavnica = Prijavnica.objects.filter(id = request.data.get('prijavnica')).update(status = request.data.get('status'))

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(
                {"res": "Nisi administrator"},
                status=status.HTTP_200_OK
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserAdminSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
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

class Logupisa(viewsets.ModelViewSet):

    serializer_class = LOG_upisaSerializer
    queryset = LOG_upisa.objects.all()
    permission_classes = [IsAuthenticated]