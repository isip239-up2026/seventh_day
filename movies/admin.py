from django.contrib import admin
from .models import Genre, Director, Movie, Review, Watchlist


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display  = ["name", "birth_year"]
    search_fields = ["name"]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display  = ["title", "year", "director", "duration"]
    list_filter   = ["genres", "year"]
    search_fields = ["title", "director__name"]
    filter_horizontal = ["genres"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author_name", "movie", "rating", "created_at"]
    list_filter  = ["rating"]


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ["movie", "ip_address", "created_at"]
