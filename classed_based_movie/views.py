from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.contrib.auth.models import User

from movie_app.models import Director, Movie, Review, RegistrationUser
from movie_app.serializer import DirectorSerializer, MovieSerializer, ReviewSerializer, RegistrationSerializer
from movie_app.views import send_code_email


class DirectorListAPIView(ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class MovieListAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class DirectorUpdateDeleteAPIVIew(RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    lookup_field = 'id'


class MovieUpdateDeleteAPIVIew(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_field = 'id'


class ReviewUpdateDeleteAPIVIew(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        send_code_email(user.email)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AuthorizationAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key}, status=status.HTTP_200_OK)
        return Response(data={'error': "User not found"}, status=status.HTTP_404_NOT_FOUND)


class VerifyEmailAPIView(APIView):
    def post(self, request):
        verification_code = request.data.get('code')
        email_verified = request.data.get('email')
        if verification_code and email_verified:
            user = RegistrationUser.objects.filter(email_verified=email_verified)
            if user.exists():
                user = user.first()
                if user.verification_code == verification_code:
                    user.email_verified = True
                    user.save()
                    return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Email and verification code required'}, status=status.HTTP_400_BAD_REQUEST)
