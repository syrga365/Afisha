from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import serializer, models


@api_view(['GET'])
def director_list_view(request):
    directors = models.Director.objects.all()
    data = serializer.DirectorSerializer(directors, many=True).data
    return Response(data=data)


@api_view(['GET'])
def director_details_view(request, id):
    try:
        director_id = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': "Director not found!!!"})
    data = serializer.DirectorSerializer(director_id).data
    return Response(data=data)


@api_view(['GET'])
def movie_list_view(request):
    movies = models.Movie.objects.all()
    data = serializer.MovieSerializer(movies, many=True).data
    return Response(data=data)


@api_view(['GET'])
def movie_details_view(request, id):
    try:
        movie_id = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Movie not found'})
    data = serializer.MovieSerializer(movie_id).data
    return Response(data=data)


@api_view(['GET'])
def review_list_view(request):
    reviews = models.Review.objects.all()
    data = serializer.ReviewSerializer(reviews, many=True).data
    return Response(data=data)


@api_view(['GET'])
def review_details_view(request, id):
    try:
        review_id = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Review not found'})
    data = serializer.ReviewSerializer(review_id).data
    return Response(data=data)
