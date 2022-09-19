from . import views
from django.urls import path

urlpatterns = [
    path('', views.show_all_movie),
    path('movie/<int:id_movie>', views.show_one_movie),
]
