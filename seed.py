import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kinoteka.settings")
django.setup()

from django.contrib.auth.models import User
from movies.models import Genre, Director, Movie, Review, Watchlist

Genre.objects.all().delete()
Director.objects.all().delete()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin")
    print("Создан администратор: логин=admin пароль=admin")

genres = {g: Genre.objects.create(name=g) for g in [
    "Драма", "Комедия", "Триллер", "Фантастика",
    "Боевик", "Мелодрама", "Анимация", "Криминал"
]}

directors = {
    "Кристофер Нолан": Director.objects.create(
        name="Кристофер Нолан", birth_year=1970,
        bio="Британско-американский режиссёр, сценарист и продюсер. Известен масштабными блокбастерами с нелинейным повествованием.",
        photo_url="https://i.pravatar.cc/200?img=51"),
    "Квентин Тарантино": Director.objects.create(
        name="Квентин Тарантино", birth_year=1963,
        bio="Американский режиссёр и сценарист. Известен нестандартной структурой повествования и стилизованным насилием.",
        photo_url="https://i.pravatar.cc/200?img=52"),
    "Дени Вильнёв": Director.objects.create(
        name="Дени Вильнёв", birth_year=1967,
        bio="Канадский режиссёр, один из самых востребованных постановщиков современного Голливуда.",
        photo_url="https://i.pravatar.cc/200?img=53"),
    "Мартин Скорсезе": Director.objects.create(
        name="Мартин Скорсезе", birth_year=1942,
        bio="Американский режиссёр, один из самых влиятельных кинематографистов всех времён.",
        photo_url="https://i.pravatar.cc/200?img=54"),
    "Хаяо Миядзаки": Director.objects.create(
        name="Хаяо Миядзаки", birth_year=1941,
        bio="Японский аниматор, режиссёр и мангака, сооснователь студии Studio Ghibli.",
        photo_url="https://i.pravatar.cc/200?img=55"),
    "Дэвид Финчер": Director.objects.create(
        name="Дэвид Финчер", birth_year=1962,
        bio="Американский режиссёр, известный мрачными психологическими триллерами.",
        photo_url="https://i.pravatar.cc/200?img=56"),
}

movies_data = [
    {
        "title": "Начало", "year": 2010, "duration": 148,
        "director": "Кристофер Нолан",
        "genres": ["Фантастика", "Боевик", "Триллер"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_FMjpg_UX600_.jpg",
        "description": "Опытный вор, специализирующийся на извлечении информации из снов, получает шанс искупить свои преступления, внедрив идею в сознание человека.",
        "reviews": [
            ("Асель", 5, "Лучший фильм Нолана. Смотрела три раза, каждый раз нахожу что-то новое. Финал до сих пор обсуждается."),
            ("Данияр", 4, "Очень сложная структура, но это и привлекает. Требует полного внимания."),
            ("Медина", 5, "Шедевр. Операторская работа, музыка, актёры — всё на высшем уровне."),
        ]
    },
    {
        "title": "Интерстеллар", "year": 2014, "duration": 169,
        "director": "Кристофер Нолан",
        "genres": ["Фантастика", "Драма"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX600_.jpg",
        "description": "Команда исследователей путешествует сквозь червоточину в поисках нового дома для человечества.",
        "reviews": [
            ("Руслан", 5, "Плакал в конце. Мощнейший фильм о любви и времени."),
            ("Айгерим", 4, "Научная составляющая поражает воображение. Концовка немного затянута."),
        ]
    },
    {
        "title": "Криминальное чтиво", "year": 1994, "duration": 154,
        "director": "Квентин Тарантино",
        "genres": ["Криминал", "Драма"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX600_.jpg",
        "description": "Несколько криминальных историй, связанных через сеть персонажей лос-анджелесского преступного мира.",
        "reviews": [
            ("Тимур", 5, "Классика, которую нужно смотреть каждому. Диалоги — просто шедевр."),
            ("Санжар", 4, "Нелинейное повествование поначалу сбивает с толку, но потом всё складывается."),
        ]
    },
    {
        "title": "Джанго освобождённый", "year": 2012, "duration": 165,
        "director": "Квентин Тарантино",
        "genres": ["Боевик", "Драма"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjIyNTQ5NjQ1OV5BMl5BanBnXkFtZTcwODg1MDU4OA@@._V1_FMjpg_UX600_.jpg",
        "description": "Освобождённый раб отправляется на юг США, чтобы спасти свою жену из рук жестокого плантатора.",
        "reviews": [
            ("Нурлан", 5, "Тарантино в лучшем виде. ДиКаприо великолепен."),
        ]
    },
    {
        "title": "Прибытие", "year": 2016, "duration": 116,
        "director": "Дени Вильнёв",
        "genres": ["Фантастика", "Драма"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMTExMzU0ODcxNDheQTJeQWpwZ15BbWU4MDE1OTI4MzAy._V1_FMjpg_UX600_.jpg",
        "description": "Лингвист пытается расшифровать язык инопланетян, прибывших на Землю, пока нарастает международная напряжённость.",
        "reviews": [
            ("Жанна", 5, "Самый умный научно-фантастический фильм последних лет. Трогает до слёз."),
            ("Бекзат", 4, "Медленный, но очень атмосферный. Концовка переворачивает всё с ног на голову."),
        ]
    },
    {
        "title": "Бегущий по лезвию 2049", "year": 2017, "duration": 164,
        "director": "Дени Вильнёв",
        "genres": ["Фантастика", "Триллер"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BNzA1Njg4NzYxOV5BMl5BanBnXkFtZTgwODk5NjU3MzI@._V1_FMjpg_UX600_.jpg",
        "description": "Офицер полиции Лос-Анджелеса 2049 года раскрывает тайну, которая угрожает дестабилизировать общество.",
        "reviews": [
            ("Алия", 5, "Визуально один из самых красивых фильмов в истории кино. Медленно, но завораживает."),
        ]
    },
    {
        "title": "Ирландец", "year": 2019, "duration": 209,
        "director": "Мартин Скорсезе",
        "genres": ["Криминал", "Драма"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMGYyOWRmNmQtY2E0My00YjljLThhNGQtZjZlMTRlMTljMGMxXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_FMjpg_UX600_.jpg",
        "description": "Хитмен вспоминает своё участие в преступном мире в эпоху организованной преступности Америки 20-го века.",
        "reviews": [
            ("Дамир", 4, "Монументальное кино. Три с половиной часа пролетают незаметно."),
            ("Сабина", 3, "Великолепная работа, но длина ощущается. Требует терпения."),
        ]
    },
    {
        "title": "Унесённые призраками", "year": 2001, "duration": 125,
        "director": "Хаяо Миядзаки",
        "genres": ["Анимация", "Фантастика"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BMjlmZmI5MDctNDE2YS00YWE0LWE5ZWItZDBhYWQ0NTcxNWRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_FMjpg_UX600_.jpg",
        "description": "Девочка попадает в мир духов, где её родители превратились в свиней. Чтобы спасти их, ей приходится работать в волшебных банях.",
        "reviews": [
            ("Акмарал", 5, "Смотрела в детстве и смотрю сейчас. Каждый раз восхищает."),
            ("Ерлан", 5, "Лучший анимационный фильм всех времён. Миядзаки — гений."),
            ("Камила", 4, "Волшебный мир, невероятная анимация. Немного страшновато для маленьких детей."),
        ]
    },
    {
        "title": "Бойцовский клуб", "year": 1999, "duration": 139,
        "director": "Дэвид Финчер",
        "genres": ["Драма", "Триллер"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BODZkMjljYTMtNmM4OS00ZDdjLWEyYTMtOGEwZDEwM2ZlOTNiXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX600_.jpg",
        "description": "Офисный работник, страдающий бессонницей, знакомится с мыловаром и создаёт подпольный бойцовский клуб.",
        "reviews": [
            ("Марат", 5, "Переворачивает сознание. Один из лучших финалов в кино."),
            ("Толе", 4, "Брэд Питт в лучшей роли. Скрытые смыслы на каждом шагу."),
        ]
    },
    {
        "title": "Семь", "year": 1995, "duration": 127,
        "director": "Дэвид Финчер",
        "genres": ["Триллер", "Криминал"],
        "poster_url": "https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMy00OTk4LTg3NWUtNjVlNTI2ZjE3NWRiXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_FMjpg_UX600_.jpg",
        "description": "Два детектива охотятся на серийного убийцу, использующего семь смертных грехов как мотив для своих преступлений.",
        "reviews": [
            ("Арман", 5, "Атмосфера давящего города не отпускает ни на минуту. Финал — шок."),
        ]
    },
]

for m in movies_data:
    movie = Movie.objects.create(
        title=m["title"], year=m["year"], duration=m["duration"],
        director=directors[m["director"]],
        poster_url=m["poster_url"], description=m["description"]
    )
    for g in m["genres"]:
        movie.genres.add(genres[g])
    for author, rating, text in m["reviews"]:
        Review.objects.create(movie=movie, author_name=author, rating=rating, text=text)

print(f"Готово: {Genre.objects.count()} жанров, {Director.objects.count()} режиссёров, "
      f"{Movie.objects.count()} фильмов, {Review.objects.count()} рецензий.")
