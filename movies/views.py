from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Movie, Director, Review, Genre
from django.core.paginator import Paginator
from movies import forms
from django.db.models import Avg, Count


def index(request):
    movies = (Movie.objects.select_related("director")
              .prefetch_related("genres")
              .annotate(avg_rating=Avg('reviews__rating')).all())
    # Сортировка
    sort_by = request.GET.get('sort', '-year')
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
    movie_rating = Movie.objects.filter(id=movie_id).aggregate(avg_rating=Avg('reviews__rating'), count=Count('id'))
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "reviews": reviews,
        "form": forms.ReviewForm(),
        "movie_rating": movie_rating,
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


def search(request):
    query = request.GET.get("q", "").strip()
    results = []
    if query:
        results = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(director__name__icontains=query) |
            Q(genres__name__icontains=query)
        ).distinct().select_related("director").prefetch_related("genres")
    return render(request, "movies/search.html", {
        "query": query,
        "results": results,
    })


def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    movies = Movie.objects.filter(genres=genre).select_related("director").prefetch_related("genres")
    return render(request, "movies/genre.html", {
        "genre": genre,
        "movies": movies
    })

def top_movies(request):
    movies = Movie.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).filter(review_count__gt=0).order_by('-avg_rating')[:10]
    return render(request, "movies/top.html", {"movies": movies})

def director_detail(request, director_id):
    director = get_object_or_404(Director, id=director_id)
    movies = director.movies.all().annotate(avg_rating=Avg('reviews__rating'))
    total_reviews = Review.objects.filter(movie__director=director).count()
    return render(request, 'movies/director.html', {
        'director': director,
        'movies': movies,
        'total_reviews': total_reviews,
    })