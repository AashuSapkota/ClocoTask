from django.db import models

# Create your models here.
class Artists(models.Model):
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other')
    ]
    name = models.CharField(max_length=255)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255)
    first_release_year = models.CharField(max_length=4)
    no_of_albums_released = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'artist'
        verbose_name_plural = 'artists'
    