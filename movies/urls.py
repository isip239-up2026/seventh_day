from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("movie/<int:movie_id>/review/", views.add_reviews, name="add_reviews"),
    path("search/", views.search, name="search"),
    path("genre/<int:genre_id>/", views.genre_movies, name="genre_movies"),
]
