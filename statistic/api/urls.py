from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'account'

router = routers.DefaultRouter()
router.register('users', views.UserBookStatView)
router.register('airlines', views.AirlineBookStatView)

urlpatterns = [
 path('', include(router.urls)),
]
