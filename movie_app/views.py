from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from . import serializer, models


@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        directors = models.Director.objects.all()
        data = serializer.DirectorSerializer(directors, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.DirectorCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        name = request.data.get('name')

        models.Director.objects.create(name=name)

        return Response(data={'message': 'Данные отправлены!'})


@api_view(['GET', 'PUT', 'DELETE'])
def director_details_view(request, id):
    try:
        director_id = models.Director.objects.get(id=id)
    except models.Director.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': "Director not found!!!"})
    if request.method == 'GET':
        data = serializer.DirectorSerializer(director_id).data
        return Response(data=data)
    elif request.method == 'DELETE':
        director_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': 'Product has been deleted!'})
    elif request.method == 'PUT':
        serializers = serializer.DirectorCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        director_id.name = request.data.get('name')
        director_id.save()
        return Response(data=serializer.DirectorSerializer(director_id).data)


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = models.Movie.objects.all()
        data = serializer.MovieSerializer(movies, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.MovieCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        movie = models.Movie.objects.create(**request.data)
        return Response(data=serializer.MovieSerializer(movie).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', "DELETE"])
def movie_details_view(request, id):
    try:
        movie_id = models.Movie.objects.get(id=id)
    except models.Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Movie not found'})
    if request.method == 'GET':
        data = serializer.MovieSerializer(movie_id).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializers = serializer.MovieCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        movie_id.title = request.data.get('title')
        movie_id.description = request.data.get('description')
        movie_id.duration = request.data.get('duration')
        movie_id.director = request.data.get('director')
        movie_id.save()
        return Response(data=serializer.MovieSerializer(movie_id).data)
    elif request.method == 'DELETE':
        movie_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': "Product has been deleted!!!"})


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        reviews = models.Review.objects.all()
        data = serializer.ReviewSerializer(reviews, many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        serializers = serializer.ReviewCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        review = models.Review.objects.create(**request.data)
        return Response(data=serializer.ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', "DELETE"])
def review_details_view(request, id):
    try:
        review_id = models.Review.objects.get(id=id)
    except models.Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'Review not found'})
    if request.method == 'GET':
        data = serializer.ReviewSerializer(review_id).data
        return Response(data=data)
    elif request.method == 'PUT':
        serializers = serializer.ReviewCreateUpdateSerializer(data=request.data)
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        review_id.text = request.data.get('text')
        review_id.movie = request.data.get('movie')
        review_id.stars = request.data.get('stars')
        return Response(data=serializer.ReviewSerializer(review_id).data)
    elif request.method == 'DELETE':
        review_id.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': "Product has been deleted"})

