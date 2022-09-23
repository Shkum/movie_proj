from django.contrib import admin
from .models import Movie


# Register your models here.

# Create Class for additional DB view setting on Django Admin Page
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # raring_status taked fom method below - additional field in response
    list_display = ['name', 'rating', 'year', 'budget', 'rating_status']
    list_editable = ['rating', 'year', 'budget']
    ordering = ['rating', 'name']  # sorting by ...
    list_per_page = 3  # Quantity of movies in list per one page

    # may use decorator instead of below method
    # admin.site.register(Movie, MovieAdmin)  # - registering our models and classes for Django Admin page


# mov from method below is instance of class Movie (to see all attribust variable has to be annotated) !!!!!!
    def rating_status(self, mov: Movie):
        if mov.rating <= 50:
            return 'poor movie'
        if mov.rating <= 75:
            return 'so-so movie'
        if mov.rating <= 85:
            return 'Good movie'
        return 'Top movie'
