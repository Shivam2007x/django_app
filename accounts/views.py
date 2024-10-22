from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from .serializers import ProfileSerializer
from django.views.decorators.csrf import csrf_exempt

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        print(request.headers) 
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            # Optionally create a new profile with default values
            profile = Profile.objects.create(
                user=user,
                first_name=user.first_name or '',
                last_name=user.last_name or '',
                email=user.email or '',
                dob=None,  # Default value or logic to handle missing DOB
                gender='Not specified'  # Default value for gender
            )
            return Response({'message': 'Profile created', 'profile': ProfileSerializer(profile).data}, status=201)

        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=200)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
class LoginView(APIView):
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    # Allow any user (even unauthenticated) to access this view
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        email = request.data.get('email')
        dob = request.data.get('dob')
        gender = request.data.get('gender')

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user and associated profile
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            dob=dob,
            gender=gender
        )
           # Generate JWT tokens for the new user
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Registration successful',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

        # Log the user in automatically after registration
        login(request, user)
        return Response({'message': 'Registration and login successful'}, status=status.HTTP_201_CREATED)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
