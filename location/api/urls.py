from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'location'

router = routers.DefaultRouter()
router.register('timezones', views.TimezoneViewSet)
router.register('cities', views.CityViewSet)
router.register('regions', views.RegionViewSet)
router.register('countries', views.CountryViewSet)

urlpatterns = [
 path('', include(router.urls)),
]
