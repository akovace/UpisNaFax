from django.db import models
from django.conf import settings
from model_utils import Choices
from django.contrib.auth.models import User

class VrstaSmjera(models.Model):
    naziv_smjera = models.CharField(max_length=200)
    kvota = models.IntegerField()
    def __str__(self):
        return self.naziv_smjera

class Prijavnica(models.Model):
    student = models.ForeignKey(User, related_name='prijave', on_delete=models.CASCADE)
    datum_rodjenja = models.DateTimeField()
    mjesto_rodjenja = models.CharField(max_length=200)
    zavrsena_skola = models.CharField(max_length=200)
    molba_za_upis_na_smjer = models.TextField()
    odabir_smjera = models.ForeignKey(VrstaSmjera, on_delete=models.CASCADE)
    dokument_o_zavrsenoj_skoli = models.FileField(upload_to='dokumetiskola')
    prosjek_ocjena = models.FloatField()
    ocjena_na_maturi = models.FloatField()
    STATUSES = Choices(
        ('0', 'U obradi'),
        ('1', 'Odobreno'),
        ('2', 'Odbijeno'))
    status = models.CharField(max_length=1, choices=STATUSES, default='0')

    datum_kriranja = models.DateTimeField('date published')
    def __str__(self):
        return self.molba_za_upis_na_smjer

class Predmeti(models.Model):
    naziv_predmeta = models.CharField(max_length=200)
    smjer = models.ForeignKey(VrstaSmjera, related_name='predmeti', on_delete=models.CASCADE)
    ECTS = models.IntegerField()
    opis_predmeta = models.TextField()
    def __str__(self):
        return self.naziv_predmeta

class LOG_upisa(models.Model):
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    prijavnica = models.ForeignKey(Prijavnica, on_delete=models.CASCADE)
    opis_odobrenja = models.TextField()
    STATUSES = Choices(
        ('1', 'Odobreno'),
        ('2', 'Odbijeno'))
    status = models.CharField(max_length=1, choices=STATUSES, blank=True)
    vrijeme_odobrenja = models.DateTimeField('date published')
    def __str__(self):
        return self.opis_odobrenja
