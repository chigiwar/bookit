from django.contrib import admin
from .models import Airline, Airport, Flight, Book, Route


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'flight')
    search_fields = ('owner', 'flight')


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Flight)
class AirlineFlight(admin.ModelAdmin):
    list_display = ('id', 'route', 'airline', 'takeoff_time', 'landing_time')


for booking_model in (Airport, Route):
    admin.site.register(booking_model)
