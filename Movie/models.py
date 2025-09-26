from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Choices
GENRE_CHOICES = [
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Horror', 'Horror'),
    ('Romance', 'Romance'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Documentary', 'Documentary'),
]

PLATFORM_CHOICES = [
    ('Netflix', 'Netflix'),
    ('Prime Video', 'Prime Video'),
    ('Disney+ Hotstar', 'Disney+ Hotstar'),
    ('HBO Max', 'HBO Max'),
    ('Other', 'Other'),
]

STATUS_CHOICES = [
    ('Watching', 'Watching'),
    ('Completed', 'Completed'),
    ('Wishlist', 'Wishlist'),
]

class Movie(models.Model):
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    episodes_total = models.PositiveIntegerField(null=True, blank=True)
    episodes_watched = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies", null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.platform})"

    def progress_percentage(self):
        if self.episodes_total:
            return (self.episodes_watched / self.episodes_total) * 100
        return None

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2, decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    comment = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/5)"

