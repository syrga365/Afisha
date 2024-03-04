import random

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializer, models
from .serializer import RegistrationSerializer


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


@api_view(['POST'])
def authorization(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'key': token.key}, status=status.HTTP_200_OK)
        return Response(data={'error': "User not found"},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def registration(request):
    if request.method == 'POST':
        serializers = RegistrationSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        send_code_email(user.email)
        return Response(serializers.data, status=status.HTTP_201_CREATED)


def send_code_email(email):
    code = ''.join([str(random.randint(0, 9)) for _ in range(5)])
    subject = 'Verification Code'
    message = f'Your verification code is: {code}'
    sender = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, sender, recipient_list)


@api_view(['POST'])
def verify_email(request):
    if request.method == 'POST':
        code = request.data.get('code')
        email = request.data.get('email')

        if code and email:
            user = models.RegistrationUser.objects.filter(email=email)
            if user.exists():
                user = user.first()
                if user.verification_code == code:
                    user.email_verified = True
                    user.save()
                else:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Email and verification code required'}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_reviews(request):
    reviews = models.Review.objects.filter(user=request.user)
    serializers = serializer.ReviewSerializer(reviews, many=True)
    return Response(data=serializers.data)
