from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import RegisteredUser
from .forms import ProfilePictureForm,ProfileUpdateForm
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def account(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']

        try:
            user_data = RegisteredUser.objects.get(id=user_id)
            return render(request, 'account.html', {'user_data': user_data})
        except RegisteredUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login_view')
    else:
        return redirect('login_view')


def home(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']

        try:
            user_data = RegisteredUser.objects.get(id=user_id)
            return render(request, 'home.html', {'user_data': user_data})
        except RegisteredUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login_view')
    else:
        return redirect('login_view')

def pic_upload(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        try:
            user_data = RegisteredUser.objects.get(id=user_id)

            if request.method == 'POST':
                form = ProfilePictureForm(request.POST, request.FILES, instance=user_data)
                if form.is_valid():
                    # Get the uploaded image
                    uploaded_image = request.FILES['img']

                    # Save the image to the media folder
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL)
                    saved_image_name = fs.save(uploaded_image.name, uploaded_image)

                    # Update the user data with the saved image name
                    user_data.img = saved_image_name
                    user_data.save()

                    return redirect('home')
                else:
                    # If form is not valid, show reasons for failure
                    messages.error(request, 'Image upload failed. Please check the following reasons:')
                    for field, errors in form.errors.items():
                        messages.error(request, f'{field}: {", ".join(errors)}')

            return redirect('home')
        except RegisteredUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login_view')
    else:
        return redirect('login_view')
    
def profile_update(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']

        try:
            user_data = RegisteredUser.objects.get(id=user_id)

            if request.method == 'POST':
                form = ProfileUpdateForm(request.POST, request.FILES, instance=user_data)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Profile updated successfully.')
                    return redirect('account')

            form = ProfileUpdateForm(instance=user_data)
            return render(request, 'account.html', {'form': form, 'user_data': user_data})
        except RegisteredUser.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return redirect('login_view')
    else:
        return redirect('login_view')

def register_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        pincode = request.POST.get('pincode')
        number = request.POST.get('number')
        address = request.POST.get('address')
        password = request.POST.get('password')

        # Validations
        if not name or not email or not username or not pincode or not number or not address or not password:
            return render(request, 'register.html', {'error': 'All fields are required'})

        try:
            # Save the user to the database
            registered_user = RegisteredUser(
                name=name,
                email=email,
                username=username,
                pincode=pincode,
                number=number,
                address=address,
            )
            registered_user.set_password(password)  # Set the password using set_password method
            registered_user.save()

            messages.success(request, 'User registered successfully. Please login!')

            return render(request, 'login.html')  # Redirect to a success page or login page

        except IntegrityError as e:
            # unique constraint violation
            messages.error(request, 'A user already exists with the credentials. Please try login.')
            return render(request, 'register.html', {'error': 'User registration failed'})

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #different variable name to avoid conflicts.
        user_to_login = authenticate(request, username=username, password=password)

        if user_to_login is not None:
            login(request, user_to_login)
            
            # Store user information in the session
            request.session['user_id'] = user_to_login.id
            request.session['username'] = user_to_login.username

            messages.success(request, 'Login successful.')
            return redirect('home')  # Redirect to the home page after login
        else:
            # Exception handling
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    
    # Destroy the session
    request.session.flush()

    messages.success(request, 'Logout successful.')
    return redirect('index')

