"""upisnafax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from upisi.views import Odobrenja, Korisnik, StudentiPrijave, Registracija,PrijavnicaPregled, PrijavnicaZaUpis, UserViewSet, GroupViewSet, VrstaSmjeraPregled, Predmeti, Logupisa

# izvor za JWT
# https://medium.com/django-rest/django-rest-framework-jwt-authentication-94bee36f2af8

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'prijavnica1', PrijavnicaPregled, basename='PrijavnicaPregled')
router.register(r'vrstasmjera', VrstaSmjeraPregled, basename='vrstasmjera-detail')
router.register(r'predmeti', Predmeti, basename='predmeti-detail')
router.register(r'logupisa', Logupisa, basename='logpisa')

#router.register(r'product', ProductViewSet, basename='Product')
#router.register(r'image', ImageViewSet, basename='Image')

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api-auth/', include('rest_framework.urls'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('registracija/', Registracija.as_view()),
    path('prijavnica/', PrijavnicaZaUpis.as_view(), name='prijavnica-detail'),
    path('studentiprijave/', StudentiPrijave.as_view(), name='studentiprijav-detail'),
    path('odobrenje/', Odobrenja.as_view()),
    path('korisnik/<int:user_id>/', Korisnik.as_view()),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
