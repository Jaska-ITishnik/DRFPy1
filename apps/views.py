from django.contrib.auth import login, logout
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema

from apps.models import Task
from apps.serializers import (
    CsrfTokenSerializer,
    LoginResponseSerializer,
    LoginSerializer,
    RegisterModelSerializer,
    TaskModelSerializer,
    UserPublicModelSerializer,
)


# Create your views here.
class TaskModelViewSet(ModelViewSet):
    serializer_class = TaskModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=RegisterModelSerializer,
        responses={201: UserPublicModelSerializer},
    )
    def post(self, request):
        serializer = RegisterModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserPublicModelSerializer(user).data, status=status.HTTP_201_CREATED)


class CsrfTokenView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(responses={200: CsrfTokenSerializer})
    def get(self, request):
        return Response({"csrfToken": get_token(request)})


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginResponseSerializer},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        response_data = UserPublicModelSerializer(user).data
        response_data["csrfToken"] = get_token(request)
        return Response(response_data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses={204: None})
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
