from .models import User,  Admin,  Category
import json
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from uuid import uuid4
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login



from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from django.contrib import messages
from django.shortcuts import render
from .models import Movie
from django.core.paginator import Paginator

from django.shortcuts import render
from .models import Movie
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Subcategory







# Category Views


from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Category

def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'list_categories.html', {'categories': categories})
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        # Create and save the new category
        Category.objects.create(name=name, description=description)
        
        # Redirect to the categories list page after adding the category
        return redirect('list_categories')
    
    return render(request, 'admin/add_category.html')


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        return redirect('list_categories')

    return render(request, 'admin/edit_category.html', {'category': category})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('list_categories')
    return render(request, 'admin/delete_category.html', {'category': category})




# Index View
def index(request):
    return render(request, 'index.html')

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'].strip().lower()
        phone = request.POST['phone']
        address = request.POST['address']
        role = request.POST['role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        hashed_password = make_password(password)

        try:
            if role == 'user':
                user = User(username=username, email=email, phone=phone, address=address, password=hashed_password, role=role)
                user.save()
            elif role == 'theatre_owner':
                user = User(username=username, email=email, phone=phone, address=address, password=hashed_password, role=role)
            else:
                return render(request, 'register.html', {'error': 'Invalid role selected'})

            user.save()
            return redirect('login')
        except Exception as e:
            return render(request, 'register.html', {'error': str(e)})

    return render(request, 'register.html')

# View Customers
def view_customers(request):
    customers = User.objects.filter(is_superuser=False)  
    context = {
        'customers': customers
    }
    return render(request, 'admin/view_customers.html', context)

# views.py
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User  # Ensure this is your custom user model

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Check if admin
        if username == 'tansya' and password == 'tansya@23':
            return redirect('admin_dashboard')

        # Authenticate user using Django's built-in authentication system
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            if user.role == 'user':
                return redirect('user_dashboard')
            elif user.role == 'theatre_owner':
                return redirect('theatre_owner_dashboard')

        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movie

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def user_dashboard(request):
    user = request.user
    # Fetch movies and other data as needed
    movies = []  # Replace with actual queryset or list of movies
    return render(request, 'user_dashboard.html', {'user': user, 'movies': movies})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required





# Admin Dashboard
def admin_dashboard(request):
    log_entries = LogEntry.objects.all()
    return render(request, 'admin/admin_dashboard.html', {'log_entries': log_entries})

# Other Views


def contact(request):
    return render(request, 'contact.html')


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import FileSystemStorage
from .models import Movie, Category

def list_movies(request):
    movies = Movie.objects.all()
    return render(request, 'list_movies.html', {'movies': movies})
# views.py

from datetime import timedelta
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        release_date = request.POST.get('release_date')
        description = request.POST.get('description')
        poster_image = request.FILES['poster']
        director = request.POST.get('director')
        duration_str = request.POST.get('duration')
        price = request.POST.get('price')

        # Convert duration from string to timedelta
        hours, minutes = map(int, duration_str.split(':'))
        duration = timedelta(hours=hours, minutes=minutes)

        category = Category.objects.get(id=category_id)

        Movie.objects.create(
            title=title,
            category=category,
            release_date=release_date,
            description=description,
            poster=poster_image,
            director=director,
            duration=duration,
            price=price,
        )

        return redirect('list_movies')  # Redirect to the list of movies after adding

    categories = Category.objects.all()
    return render(request, 'admin/add_movie.html', {'categories': categories})


from datetime import timedelta

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        movie.title = request.POST['title']
        movie.category_id = request.POST['category']
        movie.release_date = request.POST['release_date']
        movie.description = request.POST['description']
        movie.director = request.POST['director']
        movie.price = request.POST['price']
        
        duration_str = request.POST['duration']
        hours, minutes = map(int, duration_str.split(':'))
        movie.duration = timedelta(hours=hours, minutes=minutes)
        
        if 'poster' in request.FILES:
            movie.poster = request.FILES['poster']
        
        movie.save()
        return redirect('list_movies')
    
    return render(request, 'admin/edit_movie.html', {'movie': movie, 'categories': categories})


def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('list_movies')
    return render(request, 'admin/delete_movie.html', {'movie': movie})

# myapp/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Movie  # Import your Movie model
@login_required
def user_profile(request):
    user = request.user
    # Print or log user attributes to debug
    print(user.name)
    
    movies = Movie.objects.all()
    
    context = {
        'user': user,
        'movies': movies,
    }
    
    return render(request, 'user_profile.html', context)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Update the user object
        user = request.user
        user.username = username
        user.email = email
        user.phone = phone
        user.address = address
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    return render(request, 'update_profile.html')

@login_required
def user_profile(request):
    # Fetch the user profile data and pass it to the template
    user = request.user
    # Assuming you fetch movies elsewhere or use a different approach
    movies = [] # Replace with actual query to get movies
    return render(request, 'user_profile.html', {'user': user, 'movies': movies})

from django.shortcuts import render
from .models import Category  # Import your Category model

def list_categories_for_users(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'list_categories_for_users.html', context)



# views.py
from django.shortcuts import render
from .models import Movie

def movie_category(request, category):
    # Filter movies by category
    movies = Movie.objects.filter(category__name=category)
    
    # Pass movies to template
    return render(request, 'movie_category.html', {'category': category, 'movies': movies})

from django.shortcuts import render
from .models import Theatre

def list_theatres(request):
    theatres = Theatre.objects.all()
    return render(request, 'list_theatres.html', {'theatres': theatres})
# Add Theatre View
from django.shortcuts import render, redirect
from .models import Theatre, User

def add_theatre(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        total_seats = request.POST['total_seats']
        theatre_owner_id = request.POST['theatre_owner']

        try:
            theatre_owner = User.objects.get(id=theatre_owner_id, role='theatre_owner')
            Theatre.objects.create(name=name, location=location, total_seats=total_seats, theatre_owner=theatre_owner)
            return redirect('list_theatres')  # Redirect to theatre list or any other page
        except User.DoesNotExist:
            return render(request, 'add_theatre.html', {'error': 'Selected owner does not exist or is not a theatre owner'})

    owners = User.objects.filter(role='theatre_owner')
    return render(request, 'admin/add_theatre.html', {'owners': owners})



from django.shortcuts import render

def theatre_owner_dashboard(request):
    return render(request, 'theatre_owner/theatre_owner_dashboard.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Theatre

def edit_theatre(request, pk):
    theatre = get_object_or_404(Theatre, pk=pk)
    
    if request.method == 'POST':
        # Directly handle POST data (in practice, you should validate the data)
        theatre.name = request.POST.get('name', theatre.name)
        theatre.location = request.POST.get('location', theatre.location)
        theatre.total_seats = request.POST.get('total_seats', theatre.total_seats)
        theatre.save()
        return redirect('list_theatres')

    return render(request, 'admin/edit_theatre.html', {'theatre': theatre})

def delete_theatre(request, pk):
    theatre = get_object_or_404(Theatre, pk=pk)
    
    if request.method == 'POST':
        theatre.delete()
        return redirect('list_theatres')

    return render(request, 'admin/delete_theatre.html', {'theatre': theatre})

from django.shortcuts import render
from .models import Theatre  # Import your Theatre model

def user_theatre_list(request):
    theatres = Theatre.objects.all()  # Fetch all theatres
    return render(request, 'user_theatre_list.html', {'theatres': theatres})

from django.shortcuts import render
from .models import Showtime

def showtime_list(request):
    showtimes = Showtime.objects.all()
    return render(request, 'showtime_list.html', {'showtimes': showtimes})


# views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Showtime
from datetime import datetime

def add_showtime(request):
    if request.method == 'POST':
        time_str = request.POST.get('time')
     
        show_amount = request.POST.get('show_amount')

        if time_str  and show_amount:
            try:
                # Parse the time string to a time object
                time = datetime.strptime(time_str, '%I:%M %p').time()  # Extract only the time part

                # Create a new Showtime instance
                showtime = Showtime(
                    time=time,
                     # This is now a text field
                    show_amount=show_amount
                )
                showtime.save()
                return redirect('showtime_list')
            except ValueError:
                return HttpResponse('Invalid time format', status=400)
    
    return render(request, 'admin/add_showtime.html')



from django.shortcuts import render, get_object_or_404, redirect
from .models import Showtime
from django.utils.dateparse import parse_datetime
from datetime import datetime

def edit_showtime(request, pk):
    showtime = get_object_or_404(Showtime, pk=pk)
    
    if request.method == 'POST':
        time_str = request.POST.get('time')
        category = request.POST.get('category')
        show_amount = request.POST.get('show_amount')

        if time_str and category and show_amount:
            try:
                time = datetime.strptime(time_str, '%I:%M %p')  # Adjust format as needed

                showtime.time = time
                showtime.show_amount = show_amount
                showtime.save()
                return redirect('showtime_list')
            except ValueError:
                return HttpResponse('Invalid time format', status=400)

    context = {'showtime': showtime}
    return render(request, 'admin/edit_showtime.html', context)


from django.shortcuts import get_object_or_404, redirect
from .models import Showtime

def delete_showtime(request, pk):
    showtime = get_object_or_404(Showtime, pk=pk)
    if request.method == 'POST':
        showtime.delete()
        return redirect('showtime_list')
    return render(request, 'admin/delete_showtime.html', {'showtime': showtime})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse

User = get_user_model()

@login_required
def theatre_owner_profile(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        user.name = name
        user.email = email
        user.phone = phone
        user.save()
        return redirect('theatre_owner_profile')

    return render(request, 'theatre_owner/theatre_owner_profile.html', {'user': user})
