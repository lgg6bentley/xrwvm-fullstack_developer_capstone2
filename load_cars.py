import json
from djangoapp.models import CarMake, CarModel

with open('car_records.json') as f:
    data = json.load(f)

for item in data:
    make_name = item["make"]
    car_make, _ = CarMake.objects.get_or_create(name=make_name)
    
    CarModel.objects.create(
        make=car_make,
        name=item["model"],
        type=item["type"],
        year=item["year"],
        image_url=item.get("image_url", "")
    )

print("✅ Car records loaded!")