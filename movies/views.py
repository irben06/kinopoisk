from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponseServerError
from django.http import JsonResponse, HttpResponse

# Create your views here.
from .models import Movie, Actor, Genre, Rating
from django.shortcuts import get_object_or_404
from .forms import ReviewForm, RatingForm




# class MoviesView(View):
#     # "Список фильмов"
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movies.html", {"movies": movies})
    
# class MovieDetailView(View):
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, "movies/moviesingle.html", {"movie": movie})
    
# def get_categories():
#     categories = Category.objects.all()
#     return categories

def movies(request):
    # Список фильмов
    movies = Movie.objects.filter(draft=False)
    genres = Genre.objects.all()
    # years = movies.values("year")
    years = movies.values("year").distinct()

    selected_years = request.GET.getlist('year')
    selected_genres = request.GET.getlist('genre')
    
    if selected_years and selected_genres:
        movies = Movie.objects.filter(year__in=selected_years, genres__in=selected_genres, draft=False).distinct()
    elif selected_years:
        movies = Movie.objects.filter(year__in=selected_years, draft=False)
    elif selected_genres:
        movies = Movie.objects.filter(genres__in=selected_genres, draft=False).distinct()
    else:
        movies = Movie.objects.filter(draft=False)
    
    context = {
        'movies': movies,
        'genres': genres,
        'years': years,
    }
    return render(request, 'movies/movies.html', context)




# def movie_detail(request, slug):
#     # Полное описание фильма
#     movie = get_object_or_404(Movie, url=slug)
#     context = {
#         'movie': movie,
#     }
#     return render(request, 'movies/moviesingle.html', context)

def movie_detail(request, slug):
    # Полное описание фильма
    movie = get_object_or_404(Movie, url=slug)
    try:
        # Пытаемся получить рейтинг фильма, если он есть
        rating = Rating.objects.get(movie_id=movie)
    except Rating.DoesNotExist:
        # Если рейтинг не найден, устанавливаем его в None
        rating = None
    
    # Создаем экземпляр формы
    star_form = RatingForm()

    # Добавляем форму в контекст
    context = {
        'movie': movie,
        'star_form': star_form,
        'rating': rating,
    }
    return render(request, 'movies/moviesingle.html', context)


def add_review(request, pk):
    # Отзывы
    form = ReviewForm(request.POST)
    movie = Movie.objects.get(id=pk)
    if form.is_valid():
        form = form.save(commit=False)
        if request.POST.get("parent", None):
            form.parent_id = int(request.POST.get("parent"))
        form.movie = movie
        form.save()
        return redirect('movies:movie_detail', slug=movie.url)
    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})


def actorview(request, slug):
    # Инфо о актере или режисере
    actor = Actor.objects.get(name=slug)
    context = {
        'actor': actor,
    }
    return render(request, 'movies/actor.html', context)


class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)
    

    
# def get_queryset(request):
#     try:
#         years = request.GET.getlist("year")
#         queryset = Movie.objects.filter(year__in=years)
#         return queryset
#     except Exception as e:
#         return HttpResponseServerError(f"An error occurred: {e}")

# def get_queryset(request):
#     try:
#         years = [int(year) for year in request.GET.getlist("year")]
#         queryset = Movie.objects.filter(year__in=years)
#         return queryset
#     except Exception as e:
#         return HttpResponseServerError(f"An error occurred: {e}")