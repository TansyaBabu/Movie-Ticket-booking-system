from django.contrib import admin
from .models import Category, Movie

class MovieAdmin(admin.ModelAdmin):
  list_display = ('id', 'title', 'release_date', 'description', 'poster', 'director', 'duration', 'price')
  search_fields = ('title', 'director')
  list_filter = ('category', 'release_date')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Movie, MovieAdmin)





from django.contrib import admin
from .models import Showtime

class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ('showtime_id', 'time', 'show_amount')  # List display fields

admin.site.register(Showtime, ShowtimeAdmin)
