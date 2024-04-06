from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponseServerError

# Create your views here.
from .models import Movie, Actor, Genre
from django.shortcuts import get_object_or_404
from .forms import ReviewForm




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




def movie_detail(request, slug):
    # Полное описание фильма
    movie = get_object_or_404(Movie, url=slug)
    context = {
        'movie': movie,
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