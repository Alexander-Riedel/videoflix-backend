"""
auth_app.api.serializers
~~~~~~~~~~~~~~~~~~~~~~~~

This module contains serializers for user registration, login,
password reset, and password confirmation in the authentication workflow.
"""

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

GENERIC_ERROR = "Please check your input and try again."


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Includes password confirmation
    and validation logic.
    """
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
        """
        Ensure password matches confirmation and meets validation rules.
        """
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError(GENERIC_ERROR)

        try:
            validate_password(data['password'])
        except Exception:
            raise serializers.ValidationError(GENERIC_ERROR)

        return data

    def create(self, validated_data):
        """
        Create an inactive user with the provided credentials.
        """
        validated_data.pop('confirmed_password')
        return User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False
        )


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    """
    email = serializers.EmailField()


class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new password using reset token.
    """
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Ensure passwords match and meet validation rules.
        """
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError(GENERIC_ERROR)

        try:
            validate_password(data['new_password'])
        except Exception:
            raise serializers.ValidationError(GENERIC_ERROR)

        return data
