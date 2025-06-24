from .models import CarMake, CarModel

def initiate():
    make = CarMake.objects.create(name="DefaultMake", description="Auto-generated make")
    CarModel.objects.create(name="Model X", carmake=make, type="SEDAN", year=2022)
    print("Default car data initialized.")