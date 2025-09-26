from rest_framework import serializers
from Movie.models import Movie, Review
from django.contrib.auth.models import User

class MovieSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'director', 'genre', 'platform', 'status',
                  'episodes_total', 'episodes_watched', 'progress']

    def get_progress(self, obj):
        return obj.progress_percentage()  # Returns percentage if episodes_total exists


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    movie_title = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'movie', 'user', 'rating', 'comment', 'created',
                  'username', 'movie_title', 'date']

    def get_username(self, obj):
        return obj.user.username

    def get_movie_title(self, obj):
        return obj.movie.title

    def get_date(self, obj):
        return obj.created.date()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        user.save()
        return user
