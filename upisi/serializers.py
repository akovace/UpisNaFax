from django.contrib.auth.models import User, Group
from rest_framework import serializers
from upisi.models import Prijavnica, VrstaSmjera, Predmeti, LOG_upisa


class RegistracijaSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'groups']

class PrijavnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prijavnica
        #fields = ['student', 'datum_rodjenja', 'mjesto_rodjenja', 'zavrsena_skola', 'molba_za_upis_na_smjer', 'odabir_smjera', 'dokument_o_zavrsenoj_skoli', 'prosjek_ocjena', 'ocjena_na_maturi', 'status', 'datum_kriranja']
        fields = ['id','student','datum_rodjenja', 'mjesto_rodjenja', 'zavrsena_skola', 'molba_za_upis_na_smjer', 'odabir_smjera', 'dokument_o_zavrsenoj_skoli', 'prosjek_ocjena', 'ocjena_na_maturi', 'status', 'datum_kriranja']


class PredmetiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predmeti
        fields = ['id', 'naziv_predmeta', 'smjer', 'ECTS', 'opis_predmeta']

class VrstaSmjeraSerializer(serializers.HyperlinkedModelSerializer):
    predmeti = PredmetiSerializer(many=True)
    class Meta:
        model = VrstaSmjera
        fields = ['id', 'naziv_smjera', 'kvota', 'predmeti']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'groups']

class UserAdminSerializer(serializers.ModelSerializer):
    prijave = PrijavnicaSerializer(many=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups', 'prijave']



"""
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
"""


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']





class LOG_upisaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LOG_upisa
        fields = ['id', 'administrator', 'prijavnica', 'opis_odobrenja', 'status', 'vrijeme_odobrenja']
