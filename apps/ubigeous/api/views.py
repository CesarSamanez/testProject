from django_filters import filters, FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.ubigeous.api.serializer import (RegionSerializer,
                                          ProvinceSerializer,
                                          DistrictSerializer,
                                          CustomTokenObtainPairSerializer,
                                          AuthResponse,
                                          CustomLoginSerializer,
                                          RefreshTokenSerializer, UserSerializer)
from apps.ubigeous.models import Region, Province, District, User


# Custom view for obtaining access and update tokens using user credentials
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: AuthResponse,
            status.HTTP_401_UNAUTHORIZED: "Invalid credentials"
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            _email = serializer.data['email']
            _password = serializer.data['password']

            try:
                user = User.objects.get(email=_email)
                if user.check_password(_password):
                    refresh = RefreshToken.for_user(user)
                    return Response(
                        {
                            'id': user.id,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)
                        },
                        status=status.HTTP_200_OK
                    )
            except User.DoesNotExist:
                pass

            return Response(
                {
                    "message": "No active account found with the provided credentials"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: 'Successful logout'
        }
    )
    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()

        return Response(
            {
                'message': 'Successful logout'
            },
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.filter()
    filter_backends = [DjangoFilterBackend]


class RegionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    model = Region
    serializer_class = RegionSerializer
    queryset = Region.objects.filter()
    filter_backends = [DjangoFilterBackend]


# Filters model 'Province'
class ProvinceFilters(FilterSet):
    region = filters.CharFilter(field_name='region__name')

    class Meta:
        model = Province
        fields = ['region']


class ProvinceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    model = Province
    serializer_class = ProvinceSerializer
    queryset = Province.objects.filter()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProvinceFilters


# Filters model 'District'
class DistrictFilters(FilterSet):
    province = filters.CharFilter(field_name='province__name')

    class Meta:
        model = District
        fields = ['province']


class DistrictViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, ]
    model = District
    serializer_class = DistrictSerializer
    queryset = District.objects.filter()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = DistrictFilters
