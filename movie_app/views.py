from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Max, Min, Count, Avg, F, Value

# F - get field valueinside of other requests or methods

# Create your views here.
from .models import Movie, Director, Actor


def show_all_movie(request):
    # movies = Movie.objects.all()
    # movies = Movie.objects.order_by('name')  # sorting list of movies by name
    # movies = Movie.objects.order_by(F('year').asc(nulls_last=True), 'rating')  # sorting list of movies by year, decreasing, nulls last, and then by rating
    # movies = Movie.objects.order_by('name', '-budget')[:3] # sorting by name and then by budget in reverse order

    # Adding additional field for table (only in the memory, not in DB)
    movies = Movie.objects.annotate(
        true_bool=Value(True),
        false_bool=Value(False),
        str_field=Value('Hello'),
        int_field=Value(123),
        new_budget=F('budget') + 100
    )

    # for movie in movies:  # update all fields in DB
    #     movie.save()

    agg = movies.aggregate(Avg('budget'), Max('rating'), Min('rating'), Max('year'))  # - pass aggregated functions to template in return

    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg,
        'total': movies.count()
    })


def show_one_movie(request, slug_movie: str):
    # movie = Movie.objects.get(id=id_movie)
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })


def all_directors(request):
    director = Director.objects.all()
    return render(request, 'movie_app/all_directors.html', {
        'directors': director
    })


def show_director(request, slug_director: str):
    director = get_object_or_404(Director, slug=slug_director)
    return render(request, 'movie_app/one_director.html', {
        'director': director,
    })


def all_actors(request):
    actors = Actor.objects.all()
    return render(request, 'movie_app/all_actors.html', {
        'actors': actors
    })


def show_actor(request, slug_actor: str):
    actor = get_object_or_404(Actor, slug=slug_actor)
    return render(request, 'movie_app/one_actor.html', {
        'actor': actor,
    })
