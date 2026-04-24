from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Director(models.Model):
    name       = models.CharField(max_length=200, verbose_name="Имя")
    bio        = models.TextField(blank=True, verbose_name="Биография")
    birth_year = models.IntegerField(null=True, blank=True, verbose_name="Год рождения")
    photo_url  = models.URLField(blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Режиссёр"
        verbose_name_plural = "Режиссёры"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title      = models.CharField(max_length=200, verbose_name="Название")
    description= models.TextField(verbose_name="Описание")
    year       = models.IntegerField(verbose_name="Год выхода")
    director   = models.ForeignKey(Director, on_delete=models.SET_NULL,
                                   null=True, related_name="movies",
                                   verbose_name="Режиссёр")
    genres     = models.ManyToManyField(Genre, related_name="movies",
                                        verbose_name="Жанры")
    poster_url = models.URLField(blank=True, verbose_name="Постер")
    duration   = models.IntegerField(null=True, blank=True,
                                     verbose_name="Длительность (мин)")

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-year"]

    def __str__(self):
        return f"{self.title} ({self.year})"


class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    movie       = models.ForeignKey(Movie, on_delete=models.CASCADE,
                                    related_name="reviews", verbose_name="Фильм")
    author_name = models.CharField(max_length=100, verbose_name="Имя")
    rating      = models.IntegerField(choices=RATING_CHOICES, verbose_name="Оценка")
    text        = models.TextField(verbose_name="Текст рецензии")
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.author_name} → {self.movie.title} ({self.rating}★)"

    def stars(self):
        return "★" * self.rating + "☆" * (5 - self.rating)


class Watchlist(models.Model):
    movie      = models.ForeignKey(Movie, on_delete=models.CASCADE,
                                   related_name="watchlist", verbose_name="Фильм")
    ip_address = models.GenericIPAddressField(verbose_name="IP адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Список просмотра"
        verbose_name_plural = "Списки просмотра"
        unique_together = ["movie", "ip_address"]

    def __str__(self):
        return f"{self.ip_address} → {self.movie.title}"
