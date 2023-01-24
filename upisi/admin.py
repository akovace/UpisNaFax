from django.contrib import admin

from .models import VrstaSmjera, Prijavnica, Predmeti, LOG_upisa
admin.site.register(VrstaSmjera)
admin.site.register(Prijavnica)
admin.site.register(Predmeti)
admin.site.register(LOG_upisa)
