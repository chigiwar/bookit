from rest_framework import serializers
from account.api.serializers import UserSerializer
from location.api.serializers import CitySerializer
from ..models import Flight, Book, Airport, Airline, Route


class AirlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airline
        fields = ['id', 'name', 'vip']


class AirportSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Airport
        fields = ['id', 'name', 'city', 'city_id']


class RouteSerializer(serializers.ModelSerializer):
    takeoff_place = AirportSerializer(read_only=True)
    landing_place = AirportSerializer(read_only=True)
    takeoff_place_id = serializers.IntegerField(write_only=True)
    landing_place_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Route
        fields = ['id', 'takeoff_place', 'landing_place', 'takeoff_place_id', 'landing_place_id']


class FlightSerializer(serializers.ModelSerializer):

    airline = AirlineSerializer(read_only=True)
    route = RouteSerializer(read_only=True)
    airline_id = serializers.IntegerField(write_only=True)
    route_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Flight
        fields = ['id', 'route', 'takeoff_time', 'landing_time', 'airline', 'airline_id', 'route_id']


class BookSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    flight_id = serializers.IntegerField(write_only=True)
    owner_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Book
        fields = ['id', 'flight', 'owner', 'flight_id', 'owner_id', 'deleted']
