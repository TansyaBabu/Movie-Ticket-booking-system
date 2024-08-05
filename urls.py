from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import add_showtime, showtime_list,edit_showtime, delete_showtime

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
     path('login/', views.login_view, name='login'), 
   
    path('contact/', views.contact, name='contact'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
 
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
      
    path('user_profile/', views.user_profile, name='user_profile'),   # Corrected this line
     path('update_profile/', views.update_profile, name='update_profile'), 
    path('view_customers/', views.view_customers, name='view_customers'),
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('edit_movie/<int:movie_id>/', views.edit_movie, name='edit_movie'),
    path('delete_movie/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('list_movies/', views.list_movies, name='list_movies'),
     
       path('movies/<str:category>/', views.movie_category, name='movie_category'),
         path('list_theatres/', views.list_theatres, name='list_theatres'),
    path('add_theatre/', views.add_theatre, name='add_theatre'),
     path('theatre_owner_dashboard/', views.theatre_owner_dashboard, name='theatre_owner_dashboard'),
    path('edit_theatre/<int:pk>/', views.edit_theatre, name='edit_theatre'),
    path('delete_theatre/<int:pk>/', views.delete_theatre, name='delete_theatre'),
     path('user/theatres/', views.user_theatre_list, name='user_theatre_list'),
          path('showtimes/', views.showtime_list, name='showtime_list'),
             path('add_showtime/', add_showtime, name='add_showtime'),
          path('edit/<int:pk>/', edit_showtime, name='edit_showtime'),
    path('delete/<int:pk>/', delete_showtime, name='delete_showtime'),
     path('theatre_owner_profile/', views.theatre_owner_profile, name='theatre_owner_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)