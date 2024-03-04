from django.contrib import admin
from django.urls import path
from movie_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/directors/', views.director_list_view),
    path('api/v1/directors/<int:id>/', views.director_details_view),
    path('api/v1/movies/', views.movie_list_view),
    path('api/v1/movies/<int:id>/', views.movie_details_view),
    path('api/v1/reviews/', views.review_list_view),
    path('api/v1/reviews/<int:id>/', views.review_details_view),
    path('api/v1/login/', views.authorization),
    path('api/v1/register/', views.registration),
    path('api/v1/user/reviews/', views.user_reviews),
    path('api/v1/verify/', views.verify_email)
]
