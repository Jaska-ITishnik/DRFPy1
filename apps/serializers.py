from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from apps.models import Task

User = get_user_model()


class TaskModelSerializer(ModelSerializer):
    class Meta:
        model = Task
        # fields = "id", "title", "is_done", "created_at"
        fields = "id", "title", "is_done", "created_at", "owner"
        # exclude = ()
        read_only_fields = "id", "created_at", "owner"


class UserPublicModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "id", "username", "email"
        read_only_fields = fields


class RegisterModelSerializer(ModelSerializer):
    password = CharField(write_only=True, trim_whitespace=False)
    confirm_password = CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = "id", "username", "password", "confirm_password"
        read_only_fields = "id",
        extra_kwargs = {
            "username": {"required": True, "allow_blank": False},
            "password": {"required": True, "allow_blank": False},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise ValidationError({"confirm_password": "Parollar mos kelmadi"})
        if User.objects.filter(username=attrs["username"]).exists():
            raise ValidationError({"username": "Bu username allaqachon mavjud"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(Serializer):
    username = CharField(trim_whitespace=False)
    password = CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            username=attrs["username"],
            password=attrs["password"],
        )
        if user is None:
            raise ValidationError("Username yoki parol noto‘g‘ri")
        attrs["user"] = user
        return attrs


class LoginResponseSerializer(Serializer):
    id = IntegerField(read_only=True)
    username = CharField(read_only=True)
    email = CharField(read_only=True)
    csrfToken = CharField(read_only=True)


class CsrfTokenSerializer(Serializer):
    csrfToken = CharField(read_only=True)
