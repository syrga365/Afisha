from django.urls import path
from . import views

urlpatterns = [
    path('directors/', views.DirectorListAPIView.as_view()),
    path('directors/<int:id>/', views.DirectorUpdateDeleteAPIVIew.as_view()),
    path('movie/', views.MovieListAPIView.as_view()),
    path('movie/<int:id>/', views.MovieUpdateDeleteAPIVIew.as_view()),
    path('reviews/', views.ReviewListAPIView.as_view()),
    path('reviews/', views.ReviewUpdateDeleteAPIVIew.as_view()),
    path('register/', views.RegisterAPIView.as_view()),

]
