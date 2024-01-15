from django.db import models

# Create your models here.
class Company(models.Model):
    SCALE_UNKNOWN = 0
    SCALE_SMALL = 1
    SCALE_MEDIUM = 2
    SCALE_LARGE = 3

    SCALE_CHOICES = [
        (SCALE_UNKNOWN, 'Unknown'),
        (SCALE_SMALL, 'Small'),
        (SCALE_MEDIUM, 'Medium'),
        (SCALE_LARGE, 'Large'),
    ]

    name = models.CharField(max_length=30)
    description = models.TextField()
    scale = models.IntegerField(choices=SCALE_CHOICES, default=SCALE_UNKNOWN)


class Recruitment(models.Model):
    company = models.ForeignKey(Company, editable=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    reward = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    skills = models.TextField()