from rest_framework import serializers
from app.models import UserProfile
from django.utils import timezone
from rest_framework.authtoken.models import Token

class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=200, required=True)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=30,required=True)
    role = serializers.CharField(max_length=30,required=True)
    provider = serializers.CharField(max_length=50,required=True)
    
    class Meta:
        model = UserProfile
        fields = ["username", "first_name", "last_name", "email", "password", "role", "provider"]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user_instance = UserProfile(**validated_data)
        user_instance.set_password(password)
        user_instance.save()

        return user_instance

class UserProfileDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ["username", "first_name", "last_name", "email", "password", "role", "provider", "registration_datetime", "last_login", "is_active"]
        
class UserProfileDataUpdateSerializer(serializers.ModelSerializer):
    
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)
    role = serializers.CharField(max_length=30,required=False)
    provider = serializers.CharField(max_length=50,required=False)
    phone = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(max_length=255, required=False)
    city = serializers.CharField(max_length=50, required=False)
    state = serializers.CharField(max_length=50, required=False)
    zip = serializers.CharField(max_length=50, required=False)
    country = serializers.CharField(max_length=50, required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ["email", "first_name", "last_name", "role", "provider", "phone", "address", "city", "state", "zip", "country"]

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.provider = validated_data.get('provider', instance.provider)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.zip = validated_data.get('zip', instance.zip)
        instance.country = validated_data.get('country', instance.country)    
                
        instance.save()

        return instance
    
class UserDeleteSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    token = serializers.CharField(required=False)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        token = data.get('token')

        if not token and not (username and password):
            raise serializers.ValidationError("Either a token or both username and password must be provided.")

        return data