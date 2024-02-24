from rest_framework import serializers
from . import models


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
        fields = 'title'.split()


class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = models.Review
        fields = 'id movie text rating'.split()
