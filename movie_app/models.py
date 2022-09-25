from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()


class Movie(models.Model):
    EUR = 'EUR'
    USD = 'USD'
    UAH = 'UAH'

    CURRENCY_CHOICES = [
        ('EUR', 'Euro'),
        ('USD', 'Dollar'),
        ('UAH', 'Hryvna'),
    ]


    name = models.CharField(max_length=40)
    rating = models.IntegerField()
    year = models.IntegerField(null=True, blank=True)
    budget = models.IntegerField(default=1000000)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=EUR)
    slug = models.SlugField(default='', null=False)

    # method for creating slug name - currently replaced by prepopulated_fields = {'slug': ('name',)} at admin.py
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.rating}%'

    def get_url(self):
        return reverse('movie-detail', args=[self.slug])



