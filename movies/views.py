from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Avg
from .models import Movie, Director, Review
from movies import forms


def index(request):
    # Сортировка
    sort_by = request.GET.get('sort', '-year')

    movies = Movie.objects.select_related("director").prefetch_related("genres").annotate(
        avg_rating=Avg('reviews__rating')
    )

    if sort_by == 'title':
        movies = movies.order_by('title')
    elif sort_by == '-title':
        movies = movies.order_by('-title')
    elif sort_by == 'year':
        movies = movies.order_by('year')
    elif sort_by == '-year':
        movies = movies.order_by('-year')
    elif sort_by == 'avg_rating':
        movies = movies.order_by('-avg_rating')
    else:
        movies = movies.order_by(sort_by)

    # Пагинация
    paginator = Paginator(movies, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "movies/index.html", {
        "page_obj": page_obj,
        "current_sort": sort_by
    })


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "reviews": reviews,
        "form": forms.ReviewForm()
    })


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