from rest_framework import serializers
from account.api.serializers import UserSerializer
from account.models import User
from booking.api.serializers import AirlineSerializer
from booking.models import Airline


class UserStatSerializer(UserSerializer):
    count_books = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'group', 'vip', 'count_books']


class AirlineStatSerializer(AirlineSerializer):
    count_books = serializers.IntegerField(required=False)

    class Meta:
        model = Airline
        fields = ['id', 'name', 'vip', 'count_books']
