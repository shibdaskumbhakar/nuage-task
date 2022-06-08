from dataclasses import fields
from pyexpat import model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .utils import ResponseInfo
from .models import CustomUser
from rest_framework.response import Response


from rest_framework import serializers
from django.contrib.auth import get_user_model



User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'name': self.user.name})
        data.update({'email': self.user.email})
        data.update({'user_id': self.user.id})
        data.update({'active': self.user.active})
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','phone','password']
        extra_kwargs = { 'password': { 'write_only': True} }

    def validate(self, attrs):
        if len(attrs['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be 8 or more than 8 character!."})

        elif len(str(attrs['phone']))<10 or len(str(attrs['phone']))>12:
            raise serializers.ValidationError({"phone": "Phone length should be 10 to 12 digit!."})
        
        return attrs
    
    def create(self, validate_data):
        user = User.objects.create(
            name = validate_data['name'],
            email = validate_data['email'],
            phone = validate_data['phone'],
            )
        user.set_password(validate_data['password'])
        user.save()
        return user

