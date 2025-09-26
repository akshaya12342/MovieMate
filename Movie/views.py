from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth.models import User

from Movie.models import Movie, Review
from Movie.serializers import MovieSerializer, ReviewSerializer, UserSerializer


class MovieAPIView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class User_Register(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Create_review(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        u = request.user
        movie_id = request.data.get('id')
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')

        try:
            movie_obj = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        review = Review.objects.create(user=u, movie=movie_obj, rating=rating, comment=comment)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Movie_Search(APIView):
    def get(self, request):
        query = request.query_params.get('search')
        if query:
            movies = Movie.objects.filter(
                Q(title__icontains=query) |
                Q(director__icontains=query) |
                Q(genre__icontains=query) |
                Q(platform__icontains=query)
            )
            if movies.exists():
                serializer = MovieSerializer(movies, many=True)
                return Response(serializer.data)
        return Response({'msg': 'No results found'}, status=status.HTTP_200_OK)


class Movie_Filter(APIView):
    def get(self, request):
        query = request.query_params.get('filter')
        if query:
            movies = Movie.objects.filter(
                Q(genre__icontains=query) |
                Q(platform__icontains=query) |
                Q(status__icontains=query)
            )
            serializer = MovieSerializer(movies, many=True)
            if movies.exists():
                return Response(serializer.data)
        return Response({'msg': 'No results found'}, status=status.HTTP_404_NOT_FOUND)


class Review_Filter(APIView):
    def get(self, request, pk):
        try:
            movie_obj = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(movie=movie_obj)
        serializer = ReviewSerializer(reviews, many=True)
        if reviews.exists():
            return Response(serializer.data)
        return Response({'msg': 'No reviews found'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_token.delete()
        return Response({'msg': "Logout successful"}, status=status.HTTP_200_OK)


