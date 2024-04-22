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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.http import QueryDict

def movies(request):
    all_movies = Movie.objects.filter(draft=False)
    genres = Genre.objects.all()
    years = all_movies.values("year").distinct()

    # Получаем параметры из URL
    selected_years = request.GET.getlist('year')
    selected_genres = request.GET.getlist('genre')
    search_query = request.GET.get('search')

    # Применяем фильтры
    if search_query:
        movies = all_movies.filter(title__icontains=search_query)
    elif selected_years and selected_genres:
        movies = all_movies.filter(year__in=selected_years, genres__in=selected_genres).distinct()
    elif selected_years:
        movies = all_movies.filter(year__in=selected_years)
    elif selected_genres:
        movies = all_movies.filter(genres__in=selected_genres).distinct()
    else:
        movies = all_movies

    paginator = Paginator(movies, 2)
    page = request.GET.get('page')

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    # Создаем новый QueryDict для сохранения текущего состояния параметров
    query_params = QueryDict(mutable=True)
    query_params.setlist('year', selected_years)
    query_params.setlist('genre', selected_genres)
    if search_query:
        query_params['search'] = search_query
    
    context = {
        'movies': movies,
        'genres': genres,
        'years': years,
        'selected_years': selected_years,
        'selected_genres': selected_genres,
        'search_query': search_query,
        'query_params': query_params.urlencode(),  # Передаем параметры обратно в шаблон
    }
    return render(request, 'movies/movies.html', context)



def movie_detail(request, slug):
    # Полное описание фильма
    movie = get_object_or_404(Movie, url=slug)
    
    try:
        # Пытаемся получить рейтинг фильма, если он есть
        rating = Rating.objects.get(movie_id=movie)
    except Rating.DoesNotExist:
        # Если рейтинг не найден, устанавливаем его в None
        rating = None

     # Получаем доступные года и жанры
    all_movies = Movie.objects.filter(draft=False)
    genres = Genre.objects.all()
    years = all_movies.values("year").distinct()
    
    # Создаем экземпляр формы
    star_form = RatingForm()
    form = ReviewForm()

    # Добавляем форму в контекст
    context = {
        'movie': movie,
        'star_form': star_form,
        'rating': rating,
        'form': form,
        'genres': genres,
        'years': years,
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

def Search(request):
    paginate_by = 3




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