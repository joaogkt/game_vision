from django.db import models
from django_countries.fields import CountryField

class Team(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = CountryField(blank=False, null=False)
    founded_year = models.PositiveIntegerField(default=1900)
    logo = models.ImageField(upload_to='teams/', blank=True, null=True)

    def __str__(self):
        return self.name

