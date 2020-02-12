from django.db import models


class Timezone(models.Model):
    name = models.CharField(max_length=20, primary_key=True, unique=True)


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Region(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, models.CASCADE, related_name='region_country')

    def __str__(self):
        return f'{self.name} ({self.country})'


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, models.SET_NULL, related_name='city_region', blank=True, null=True)
    timezone = models.ForeignKey(Timezone, models.CASCADE, related_name='city_timezone', to_field='name')

    def __str__(self):
        return f'{self.name} ({self.region})'

    class Meta:
        unique_together = ('name', 'region')
