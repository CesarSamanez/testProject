from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.ubigeous.models import Region, Province, District, User


# Serializer to customize and add information from the user's email field to the token
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


# Serializer to display authentication response
class AuthResponse(serializers.Serializer):
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)


# Custom serializer for the user login using the fields: email and password
class CustomLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


# Serializer to manage token refresh
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


# 'User' model serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'lastname', 'email', 'username', 'password')


# 'Region' model serializer
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        exclude = ('created', 'updated')


# 'Province' model serializer
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        exclude = ('created', 'updated')

        # Control the representation of the 'region' field when serialized

    def to_representation(self, obj):
        if 'branches' not in self.fields:
            self.fields['region'] = RegionSerializer(obj, many=False)
        return super(ProvinceSerializer, self).to_representation(obj)


# 'District' model serializer
class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('created', 'updated')

    # Control the representation of the 'province' field when serialized
    def to_representation(self, obj):
        if 'branches' not in self.fields:
            self.fields['province'] = ProvinceSerializer(obj, many=False)
        return super(DistrictSerializer, self).to_representation(obj)
