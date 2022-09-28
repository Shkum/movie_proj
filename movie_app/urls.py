from . import views
from django.urls import path

urlpatterns = [
    path('', views.show_all_movie),
    path('movie/<slug:slug_movie>', views.show_one_movie, name='movie-detail'),
    path('directors', views.all_directors),
    path('directors/<slug:slug_director>', views.show_director, name='director-detail'),
    path('actors', views.all_actors),
    path('actor/<slug:slug_actor>', views.show_actor, name='actor-detail'),
]

