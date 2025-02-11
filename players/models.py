from django.db import models
import teams.models
from django_countries.fields import CountryField
from datetime import date

# Create your models here.
class Player(models.Model):
    POSITION_CHOICES = [
        ('GOL', 'Goleiro'),
        ('DEF', 'Defensor'),
        ('MEI', 'Meio-campo'),
        ('ATA', 'Atacante'),
    ]
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    # nationality = models.CharField(max_length=50)
    nationality = CountryField(blank=False, null=False)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    team = models.ForeignKey(teams.models.Team, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='players/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )