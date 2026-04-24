from django.shortcuts import render, get_object_or_404
from .models import Movie, Director


def index(request):
    movies = Movie.objects.select_related("director").prefetch_related("genres").all()
    return render(request, "movies/index.html", {"movies": movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "movies/movie_detail.html", {"movie": movie})
