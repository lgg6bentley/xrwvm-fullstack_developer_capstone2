from django.contrib import admin
from .models import CarMake, CarModel

# Register your models here.

# Registering CarMake model with the admin site
admin.site.register(CarMake)

# Registering CarModel model with the admin site
admin.site.register(CarModel)
