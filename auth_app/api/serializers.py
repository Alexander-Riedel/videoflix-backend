from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

GENERIC_ERROR = "Bitte überprüfe deine Eingaben und versuche es erneut."

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=GENERIC_ERROR
            )
        ]
    )
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirmed_password')

    def validate(self, data):
        # Passwort-Mismatch?
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(GENERIC_ERROR)
        # Passwort-Regeln (Länge, Komplexität etc.)
        try:
            validate_password(data['password'])
        except serializers.ValidationError:
            raise serializers.ValidationError(GENERIC_ERROR)
        return data

    def create(self, validated_data):
        # confirmed_password rauswerfen
        validated_data.pop('confirmed_password')
        # User anlegen, inaktiv
        return User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(GENERIC_ERROR)
        try:
            validate_password(data['new_password'])
        except serializers.ValidationError:
            raise serializers.ValidationError(GENERIC_ERROR)
        return data
