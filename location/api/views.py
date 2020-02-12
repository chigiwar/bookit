from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from booking.api.permissions import IsAdmin

from ..models import Country, Region, City, Timezone
from .serializers import CountrySerializer, RegionSerializer, CitySerializer, TimezoneSerializer


class EditMixin(
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.mixins.UpdateModelMixin
):
    pass


class CountryViewSet(viewsets.GenericViewSet, EditMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class RegionViewSet(viewsets.GenericViewSet, EditMixin):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class CityViewSet(viewsets.GenericViewSet, EditMixin):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class TimezoneViewSet(viewsets.GenericViewSet, EditMixin):
    queryset = Timezone.objects.all()
    serializer_class = TimezoneSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
