from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserRegisterSerializer, UserProfileDataSerializer, UserProfileDataUpdateSerializer, UserDeleteSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from app.models import UserProfile
from django.utils import timezone

@method_decorator(csrf_exempt, name="dispatch")
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Generate a token for the newly registered user
            token, _ = Token.objects.get_or_create(user=user)

            # Include the token in the response
            response_data = {
                'message': 'User registered successfully!! Please keep the token in a safe place as it will not be shown again.',
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'token': token.key 
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name="dispatch")   
class UserLoginAndDataView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        token_key = request.data.get('token')

        if token_key:
            # Token verification
            try:
                token = Token.objects.get(key=token_key)
                user = token.user
                user.last_login = timezone.now()
                user.save()
            except Token.DoesNotExist:
                return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
        elif (username or email) and password:
            # Username/email and password authentication
            user = authenticate(username=username, password=password) or authenticate(email=email, password=password)
            if user is not None:
                user.last_login = timezone.now()
                user.save()
            if user is None:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid request. Provide username/email and password or token.'}, status=status.HTTP_400_BAD_REQUEST)

        created = False  # Initialize created as False
        
        # Generate a token for the authenticated user (if not provided in the request)
        if not token_key:
            token, created = Token.objects.get_or_create(user=user)
        if created:
            token_key = token.key  # Get the token key only if it was created

        # Use the UserAndUserProfileSerializer for the response
        serializer = UserProfileDataSerializer(user)
        
        # Include user details and profile details in the response
        response_data = {
            'message': 'Login successful. User data retrieved successfully!!',
            'user-account-details': serializer.data,
            'phone': user.phone,  # Include phone in the response
            'address': user.address,  # Include address in the response
            'city': user.city,  # Include city in the response
            'state': user.state,  # Include state in the response
            'zip': user.zip,  # Include zip in the response
            'country': user.country,  # Include country in the response
                        
        }

        # Include the token and a message in the response only if it was created
        if created:
            response_data['token'] = token_key
            response_data['token_message'] = 'Token was not there, so it was created! Please keep it in a safe place!'

        return Response(response_data, status=status.HTTP_200_OK)

@method_decorator(csrf_exempt, name="dispatch")   
class UserProfileDataUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user_profile = UserProfile.objects.get(username=request.user.username)
        serializer = UserProfileDataUpdateSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            user_profile = serializer.save()
            response_data = {
                'message': 'Profile updated successfully!!!',
                'user': UserProfileDataUpdateSerializer(user_profile).data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
@method_decorator(csrf_exempt, name="dispatch")            
class UserDeleteView(APIView):
    
    def get_user_token(self, user):
        try:
            return Token.objects.get(user=user)
        except Token.DoesNotExist:
            return None

    def delete_user_token(self, user):
        token = self.get_user_token(user)
        if token:
            token.delete()

    def post(self, request):
        serializer = UserDeleteSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            token_key = serializer.validated_data.get('token')

            if token_key:
                # Token verification
                try:
                    token = Token.objects.get(key=token_key)
                    user = token.user
                except Token.DoesNotExist:
                    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
            elif username and password:
                # Username and password authentication
                user = authenticate(username=username, password=password)
                if user is None:
                    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid request. Provide username and password or token.'}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the user token and user
            self.delete_user_token(user)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)