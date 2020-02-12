from django.db import models
from location.models import City
from account.models import User


class Airline(models.Model):
    name = models.CharField(max_length=250)
    vip = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=250)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_airport')

    def __str__(self):
        return f'{self.name} ({self.city})'


class Route(models.Model):
    takeoff_place = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='route_takeoff_place')
    landing_place = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='route_landing_place')

    class Meta:
        unique_together = ('takeoff_place', 'landing_place')

    def __str__(self):
        return f'{self.takeoff_place} -> {self.landing_place}'


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flight_route')
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, related_name='flight_airline')
    takeoff_time = models.DateTimeField()
    landing_time = models.DateTimeField()

    def __str__(self):
        return f'{self.airline} {self.route} ({self.takeoff_time})'

    class Meta:
        ordering = ('takeoff_time', )


class RemainingBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class DeletedBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class Book(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_book')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='booked_flight')
    deleted = models.BooleanField(default=False, blank=True)
    objects = RemainingBookManager()
    deleted_objects = DeletedBookManager()
    all_objects = models.Manager()

    def __str__(self):
        return f'{self.owner} {self.flight} '
