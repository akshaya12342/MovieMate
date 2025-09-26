from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views as authtoken_views
from . import views

router = SimpleRouter()
router.register('movies', views.MovieAPIView, basename='movies')
router.register('users', views.User_Register, basename='users')

urlpatterns = [
    path('', include(router.urls)),

    # Search and filter
    path('movie_search/', views.Movie_Search.as_view(), name='movie_search'),
    path('movie_filter/', views.Movie_Filter.as_view(), name='movie_filter'),
    path('review_filter/<int:pk>/', views.Review_Filter.as_view(), name='review_filter'),

    # Authentication
    path('login/', authtoken_views.obtain_auth_token, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Create review
    path('create_review/', views.Create_review.as_view(), name='create_review'),
]
