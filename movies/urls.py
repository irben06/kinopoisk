from django.urls import path
from .views import movies, movie_detail, add_review, actorview

from .import views

app_name = 'movies'



# urlpatterns = [
#     path('', views.MoviesView.as_view(), name='index'),
#     path('<slug:slug>', views.MovieDetailView.as_view(), name='movie_detail'),
    
# ]

urlpatterns = [
    path('', movies, name='index'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    # path('filter/', get_queryset, name='filter'),
    path('<slug:slug>', movie_detail, name='movie_detail'),
    path('review/<int:pk>/', add_review, name="add_review"),
    path('actor/<str:slug>/',actorview, name='actorview'),
    
]
