from django.db import models
from django.utils import timezone

# CarMake model
class CarMake(models.Model):
    """
    Represents a car manufacturer.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the car make (e.g., 'Ford', 'Toyota')."
    )
    description = models.TextField(
        blank=True,
        help_text="A brief description of the car make."
    )

    def __str__(self):
        return self.name

# CarModel model
class CarModel(models.Model):
    """
    Represents a specific model of a car, linked to a CarMake.
    """
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('COUPE', 'Coupe'),
        ('SPORTS', 'Sports Car'),
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('ELECTRIC', 'Electric Vehicle'),
        ('HYBRID', 'Hybrid Vehicle'),
        ('LUXURY', 'Luxury Car'),
        ('OTHER', 'Other'),
    ]

    carmake = models.ForeignKey(
        CarMake,
        on_delete=models.CASCADE,
        default=1,  # Be sure a CarMake with ID=1 exists
        help_text="The car make this model belongs to."
    )
    name = models.CharField(
        max_length=100,
        help_text="The name of the car model (e.g., 'Focus', 'Camry')."
    )
    type = models.CharField(
        max_length=20,
        choices=CAR_TYPES,
        default='SEDAN',
        help_text="The type of car (e.g., 'SUV', 'Sedan')."
    )
    year = models.IntegerField(
        help_text="The manufacturing year of the car model."
    )

    def __str__(self):
        return f"{self.carmake.name} - {self.name} ({self.year})"

    class Meta:
        unique_together = ('carmake', 'name', 'year')