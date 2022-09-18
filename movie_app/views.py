from django.shortcuts import render

# Create your views here.
from . models import Movie

def show_all_movie(request):
    movies =Movie.objects.all()
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies
    })

