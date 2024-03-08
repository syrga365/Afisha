from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.contrib.auth.models import User

from . import models


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'username email'.split()


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Director
        fields = 'id name movies_count'.split()

    def get_movies_count(self, obj):
        return obj.movie.count()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Movie
        fields = 'title duration director'.split()


class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = models.Review
        fields = 'id movie text rating'.split()


class DirectorCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=5)


class MovieCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=50)
    description = serializers.CharField()
    duration = serializers.IntegerField()
    director_id = serializers.IntegerField()

    def validate_director_id(self, director_id):
        if models.Director.objects.filter(id=director_id).count() == 0:
            raise ValidationError(f'Category with id {director_id} does not exist')


class ReviewCreateUpdateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=5)
    movie = serializers.CharField(min_length=3)
    stars = serializers.IntegerField(min_value=1, max_value=5)

    def validate_movie_id(self, movie_id):
        if models.Movie.objects.filter(id=movie_id).count() == 0:
            raise ValidationError(f'Movie with id {movie_id} does not exist')
