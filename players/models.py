from django.db import models
import teams.models
from django_countries.fields import CountryField
from datetime import date
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
# from django.contrib.auth.models import User

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
    nationality = CountryField(blank=False, null=False)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    team = models.ForeignKey(teams.models.Team, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='players/', blank=True, null=True)
    # usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
        
    def save(self, *args, **kwargs):
        try:
            old_instance = Player.objects.get(pk=self.pk)
            if old_instance.photo and old_instance.photo != self.photo:
                if os.path.isfile(old_instance.photo.path):
                    os.remove(old_instance.photo.path)
        except Player.DoesNotExist:
            pass 

        super().save(*args, **kwargs)


@receiver(post_delete, sender=Player)
def delete_photo_on_player_delete(sender, instance, **kwargs):
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
