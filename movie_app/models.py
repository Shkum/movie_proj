from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.


class DressingRoom(models.Model):
    floor = models.IntegerField()
    room_number = models.IntegerField()

    def __str__(self):
        return f'Floor - {self.floor}, room - {self.room_number}'


class Actor(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)
    slug = models.SlugField(default='', null=False)
    dressing = models.OneToOneField(DressingRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.gender == self.MALE:
            return f'Actor {self.first_name} {self.last_name}'
        else:
            return f'Actress {self.first_name} {self.last_name}'

    def get_url(self):
        self.slug = slugify(self.last_name, self.last_name)
        s = reverse('actor-detail', args=[self.slug])
        return s


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    director_email = models.EmailField()
    slug = models.SlugField(default='', null=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_url(self):
        self.slug = slugify(self.last_name, self.last_name)
        s = reverse('director-detail', args=[self.slug])
        return s


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
    # connect two models one-to-many
    director = models.ForeignKey(Director, on_delete=models.PROTECT, null=True, related_name='movies')
    actors = models.ManyToManyField(Actor, related_name='movies', blank=True)

    # method for creating slug name - currently replaced by prepopulated_fields = {'slug': ('name',)} at admin.py
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.rating}%'

    def get_url(self):
        s = reverse('movie-detail', args=[self.slug])
        return s
