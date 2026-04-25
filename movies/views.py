from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Director, Review
from movies import forms
from django.db.models import Avg, Count
def index(request):
    movies = (Movie.objects.select_related("director")
              .prefetch_related("genres")
              .annotate(avg_rating=Avg('reviews__rating')).all())
    return render(request, "movies/index.html", {"movies": movies})


def movie_detail(request, movie_id):
    movie_rating = Movie.objects.filter(id=movie_id).aggregate(avg_rating=Avg('reviews__rating'), count=Count('id'))
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    return render(request, "movies/movie_detail.html", {"movie": movie, "review": reviews, "form": forms.ReviewForm(), "movie_rating": movie_rating})

def add_reviews(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                movie=movie,
                author_name=form.cleaned_data['author_name'],
                rating=int(form.cleaned_data['rating']),
                text=form.cleaned_data['text']
            )
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = forms.ReviewForm()
    return render(request, "movies/movie_detail.html", {})