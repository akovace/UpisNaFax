from django.contrib.auth.models import User, Group
from rest_framework import serializers
from upisi.models import Prijavnica, VrstaSmjera, Predmeti, LOG_upisa


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
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

class PrijavnicaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prijavnica
        fields = ['student', 'datum_rodjenja', 'mjesto_rodjenja', 'zavrsena_skola', 'molba_za_upis_na_smjer', 'odabir_smjera', 'dokument_o_zavrsenoj_skoli', 'prosjek_ocjena', 'ocjena_na_maturi', 'status', 'datum_kriranja']

class VrstaSmjeraSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VrstaSmjera
        fields = ['id', 'naziv_smjera', 'kvota']

class PredmetiSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Predmeti
        fields = ['id', 'naziv_predmeta', 'smjer', 'ECTS', 'opis_predmeta']

class LOG_upisaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LOG_upisa
        fields = ['id', 'administrator', 'prijavnica', 'opis_odobrenja', 'status', 'vrijeme_odobrenja']
