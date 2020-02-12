from django.contrib import admin
from .models import Country, Region, City, Timezone

for location_model in (Country, Region, City, Timezone):
    admin.site.register(location_model)
