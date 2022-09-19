from django.shortcuts import render

# Create your views here.
from . models import Movie

def show_all_movie(request):
    movies = Movie.objects.all()
    return render(request, 'movie_app/all_movies.html', {
        'movies': movies
    })


def show_one_movie(request, id_movie: int):
    movie = Movie.objects.get(id=id_movie)
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })
