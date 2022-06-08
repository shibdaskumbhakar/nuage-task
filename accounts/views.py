from django.shortcuts import render

from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .utils import ResponseInfo
from rest_framework import permissions

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Modified jwt token view
    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = MyTokenObtainPairSerializer



class RegisterUserView(APIView):
    """
    API for register new user
    """

    permission_classes = (permissions.AllowAny, )

    def __init__(self):
        self.response = ResponseInfo().response

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            self.response['status'] = status.HTTP_201_CREATED
            self.response['data'] = serializer.data
            self.response['message'] = 'User Succesfully created'
            return Response(self.response, status=status.HTTP_201_CREATED)
        else:
            self.response['status'] = False
            self.response['message'] = serializer.errors
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)