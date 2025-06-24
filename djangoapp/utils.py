from .models import CarMake, CarModel

def initiate():
    print("Initiating default data...")

    car_make, _ = CarMake.objects.get_or_create(
        name="Toyota", description="Japanese car manufacturer"
    )
    CarModel.objects.get_or_create(
        name="Corolla",
        carmake=car_make,
        type="SEDAN",
        year=2022
    )