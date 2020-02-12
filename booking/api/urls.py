from django.urls import path, include
from rest_framework import routers
from . import views


app_name = 'booking'

router = routers.DefaultRouter()
router.register('books', views.BookViewSet)
router.register('flights', views.FlightView)
router.register('airlines', views.AirlineView)

urlpatterns = [
 path('', include(router.urls)),
]
