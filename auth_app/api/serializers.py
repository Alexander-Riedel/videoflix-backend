from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


class RegisterSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirmed_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # 1. Prüfen, ob Passwort und Bestätigung übereinstimmen
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError("Die Passwörter stimmen nicht überein.")
        # 2. Standard-Passwort-Validierung (Länge, Komplexität etc.)
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        # Entferne confirmed_password bevor wir das User-Objekt erstellen
        validated_data.pop('confirmed_password')
        # Benutzer anlegen, aber noch inaktiv lassen
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Prüfen, ob neue Passwörter übereinstimmen
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Die Passwörter stimmen nicht überein.")
        validate_password(data['new_password'])
        return data
