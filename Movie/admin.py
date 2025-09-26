from django.contrib import admin

from Movie.models import Review,Movie

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)