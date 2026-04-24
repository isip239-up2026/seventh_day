# Кинотека — учебный проект

## Быстрый старт

```bash
pip install django
python manage.py migrate
python seed.py          # загрузить данные
python manage.py runserver
```

Открыть: http://127.0.0.1:8000  
Админка: http://127.0.0.1:8000/admin — логин `admin` / пароль `admin`

---

## Структура проекта

```
kinoteka/
├── kinoteka/               # настройки проекта
│   ├── settings.py
│   └── urls.py
├── movies/                 # приложение
│   ├── models.py           # Genre, Director, Movie, Review, Watchlist
│   ├── views.py            # index, movie_detail
│   ├── urls.py
│   ├── admin.py
│   └── templates/movies/
│       ├── base.html
│       ├── index.html
│       └── movie_detail.html
├── seed.py
└── db.sqlite3
```

## Модели

```
Genre      — name
Director   — name, bio, birth_year, photo_url
Movie      — title, description, year, director(FK), genres(M2M), poster_url, duration
Review     — movie(FK), author_name, rating(1–5), text, created_at
Watchlist  — movie(FK), ip_address, created_at
```

## Страницы

| URL | Описание |
|-----|----------|
| `/` | Список всех фильмов |
| `/movie/<id>/` | Страница фильма |

---

## Задания для студентов

### Task 1 — Жанры и фильтрация по жанру
**Файлы:** `movies/views.py`, `movies/urls.py`, `movies/templates/movies/index.html`, `movies/templates/movies/genre.html` (создать)

На главной странице жанры у фильмов нигде не выводятся. Нужно добавить их как бейджи и сделать фильтрацию.

Что сделать:
1. В `index.html` в блоке `ЗАДАНИЕ 1` вывести жанры фильма как цветные Bootstrap-бейджи через `{% for genre in movie.genres.all %}`
2. В `movie_detail.html` в блоке `ЗАДАНИЕ 1` сделать то же самое
3. Добавить маршрут `/genre/<int:genre_id>/` в `urls.py` и view `genre_movies`
4. View фильтрует фильмы: `Movie.objects.filter(genres=genre)`
5. Создать `genre.html` — список фильмов жанра, заголовок «Жанр: Триллер», счётчик фильмов
6. Бейджи жанров сделать кликабельными ссылками на страницу жанра

---

### Task 2 — Рецензии и форма добавления
**Файлы:** `movies/forms.py` (создать), `movies/views.py`, `movies/urls.py`, `movies/templates/movies/movie_detail.html`

Рецензии уже есть в БД, но нигде не выводятся. Нужно показать их и добавить форму.

Что сделать:
1. В view `movie_detail` добавить в контекст `reviews = movie.reviews.all()`
2. В шаблоне в блоке `ЗАДАНИЕ 2` вывести рецензии — имя автора, рейтинг звёздами через `{{ review.stars }}` (метод уже есть в модели), текст, дата
3. Создать `movies/forms.py` с классом `ReviewForm` — поля `author_name`, `rating` (select 1–5), `text`
4. Добавить маршрут `/movie/<int:movie_id>/review/` и view `add_review`
5. View обрабатывает POST: сохраняет рецензию, редирект обратно на страницу фильма
6. В шаблоне вывести форму с Bootstrap-стилями

---

### Task 3 — Средний рейтинг фильма
**Файлы:** `movies/views.py`, `movies/templates/movies/index.html`, `movies/templates/movies/movie_detail.html`

Нужно подсчитать средний рейтинг из рецензий и показать его на обеих страницах.

Что сделать:
1. В view `index` добавить аннотацию к queryset:
```python
from django.db.models import Avg
movies = Movie.objects.annotate(avg_rating=Avg('reviews__rating'))
```
2. В `index.html` в блоке `ЗАДАНИЕ 3` вывести рейтинг в карточке: `{{ movie.avg_rating|floatformat:1 }}★` или «Нет оценок» если `None`
3. В view `movie_detail` тоже добавить `avg_rating` через `aggregate`:
```python
from django.db.models import Avg, Count
stats = movie.reviews.aggregate(avg=Avg('rating'), count=Count('id'))
```
4. На странице фильма показать средний балл крупно и количество рецензий: «4.3★ · 12 рецензий»

---

### Task 4 — Похожие фильмы
**Файлы:** `movies/views.py`, `movies/templates/movies/movie_detail.html`

На странице фильма добавить блок «Похожие фильмы» — те у которых совпадает хотя бы один жанр.

Что сделать:
1. В view `movie_detail` получить жанры текущего фильма: `genres = movie.genres.all()`
2. Найти похожие: `related = Movie.objects.filter(genres__in=genres).exclude(id=movie.id).distinct()[:4]`
3. В шаблоне в блоке `ЗАДАНИЕ 4` вывести похожие фильмы горизонтальной строкой — постер (маленький), название, год
4. Если похожих нет — блок не показывать через `{% if related %}`
5. Добавить подпись к каждому фильму какой жанр совпал (необязательно, для тех кто быстро справится)

---

### Task 5 — Поиск фильмов
**Файлы:** `movies/views.py`, `movies/urls.py`, `movies/templates/movies/base.html`, `movies/templates/movies/search.html` (создать)

Поиск должен искать по названию фильма, имени режиссёра и жанру одновременно.

Что сделать:
1. В `base.html` в навбар добавить GET-форму с полем `q`
2. Добавить маршрут `/search/` и view `search`
3. Использовать Q-объекты:
```python
from django.db.models import Q
results = Movie.objects.filter(
    Q(title__icontains=q) |
    Q(director__name__icontains=q) |
    Q(genres__name__icontains=q)
).distinct()
```
4. Создать `search.html` — карточки результатов или «Ничего не найдено»
5. В заголовке страницы выводить запрос и количество результатов: «Нолан — найдено 3 фильма»

---

### Task 6 — Сортировка и пагинация
**Файлы:** `movies/views.py`, `movies/templates/movies/index.html`

Сортировка и пагинация должны работать вместе — при переходе на следующую страницу сортировка сохраняется.

Что сделать:
1. В view `index` добавить сортировку через `request.GET.get('sort', '-year')`:
   - по году выхода (`-year` / `year`)
   - по названию (`title`)
   - по рейтингу (нужен `annotate(avg_rating=Avg('reviews__rating'))` и сортировка по `-avg_rating`)
2. Добавить пагинацию через `Paginator` — по 4 фильма на страницу
3. В шаблоне сохранять параметр сортировки в ссылках пагинации: `?sort={{ request.GET.sort }}&page=2`
4. Подсветить активную кнопку сортировки

---

### Task 7 — Топ фильмов
**Файлы:** `movies/views.py`, `movies/urls.py`, `movies/templates/movies/top.html` (создать), `movies/templates/movies/base.html`

Что сделать:
1. Добавить маршрут `/top/` и view `top_movies`
2. В view получить фильмы отсортированные по среднему рейтингу:
```python
from django.db.models import Avg, Count
movies = Movie.objects.annotate(
    avg_rating=Avg('reviews__rating'),
    review_count=Count('reviews')
).filter(review_count__gt=0).order_by('-avg_rating')[:10]
```
3. Создать `top.html` — нумерованный список с постером, названием, годом, режиссёром и рейтингом
4. Первые три места выделить золотом, серебром, бронзой
5. В `base.html` добавить ссылку «Топ фильмов» в навбар

---

### Task 8 — Список «Хочу посмотреть»
**Файлы:** `movies/views.py`, `movies/urls.py`, `movies/templates/movies/movie_detail.html`, `movies/templates/movies/watchlist.html` (создать), `movies/templates/movies/base.html`

Без авторизации — список привязан к IP-адресу пользователя.

Что сделать:
1. Добавить маршруты `/movie/<id>/watchlist/` и `/watchlist/`
2. View `toggle_watchlist`: если фильм уже в списке — удалить, если нет — добавить. После — редирект обратно
3. IP получить через `request.META.get('REMOTE_ADDR')`
4. На странице фильма в блоке `ЗАДАНИЕ 8` показать кнопку: «+ В список» или «✓ В списке» в зависимости от наличия
5. Создать `watchlist.html` — все фильмы текущего IP в списке просмотра
6. В `base.html` добавить ссылку «Хочу посмотреть» в навбар

---

### Task 9 — Страница режиссёра
**Файлы:** `movies/views.py`, `movies/urls.py`, `movies/templates/movies/director.html` (создать), `movies/templates/movies/index.html`, `movies/templates/movies/movie_detail.html`

Что сделать:
1. Добавить маршрут `/director/<int:director_id>/` и view `director_detail`
2. View передаёт режиссёра и все его фильмы: `movies = director.movies.all()`
3. Создать `director.html` — фото, имя, год рождения, биография, список фильмов карточками
4. В `index.html` в блоке `ЗАДАНИЕ 9` сделать имя режиссёра в карточке кликабельной ссылкой
5. На странице фильма тоже сделать имя режиссёра ссылкой
6. На странице режиссёра показать общее количество рецензий на все его фильмы

---

### Task 10 — Экспорт фильма и страница 404
**Файлы:** `movies/views.py`, `movies/urls.py`, `movies/templates/movies/movie_detail.html`, `movies/templates/404.html` (создать), `kinoteka/settings.py`, `kinoteka/urls.py`

Два небольших задания в одном файле.

**Часть А — Экспорт:**
1. Добавить маршрут `/movie/<int:movie_id>/export/`
2. View `export_movie` возвращает текстовый файл для скачивания:
```python
response = HttpResponse(content_type='text/plain; charset=utf-8')
response['Content-Disposition'] = f'attachment; filename="{movie.title}.txt"'
```
3. Файл содержит: название, год, режиссёр, жанры, описание, список рецензий с оценками
4. В `movie_detail.html` добавить кнопку «Скачать информацию»
5. Если передан параметр `?format=csv` — вернуть CSV через стандартный модуль `csv`

**Часть Б — Своя страница 404:**
1. В `settings.py` выставить `DEBUG = False` и `ALLOWED_HOSTS = ['*']`
2. Создать `movies/templates/404.html` в тёмном стиле проекта — сообщение «Страница не найдена», кнопка «На главную»
3. В `views.py` добавить `def handler404(request, exception): return render(request, '404.html', status=404)`
4. В `kinoteka/urls.py` добавить `handler404 = 'movies.views.handler404'`
