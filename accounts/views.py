from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import views
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response

from drf_rw_serializers import generics as rw_generics
from rest_framework_api_key.permissions import HasAPIKey

from bridges.decorators import use_transaction

from .permissions import IsOwner, IsManager
from .models import Profile
from .filters import ProfileFilterSet

from .serializers import (
    UserReadSerializer, UserCreateSerializer, UserUpdateSerializer,
    ProfileReadSerializer, ProfileCreateSerializer, ProfileConfirmSerializer,
    ProfileUpdateSerializer, ProfileUnlockSerializer
)


class UserListView(rw_generics.CreateAPIView):

    write_serializer_class = UserCreateSerializer
    read_serializer_class = UserReadSerializer

    permission_classes = [
        HasAPIKey
    ]


class UserCurrentView(rw_generics.RetrieveUpdateDestroyAPIView):

    write_serializer_class = UserUpdateSerializer
    read_serializer_class = UserReadSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method != 'GET':
            return permissions + [IsOwner()]
        return permissions

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ProfileListView(rw_generics.ListCreateAPIView):

    write_serializer_class = ProfileCreateSerializer
    read_serializer_class = ProfileReadSerializer

    permission_classes = [
        IsAuthenticated
    ]

    filterset_class = ProfileFilterSet

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.request.method != 'GET':
            return permissions + [IsManager()]
        return permissions

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Profile.objects.none()
        qs = user.userprofiles.all()
        return qs


class ProfileConfirmView(rw_generics.CreateAPIView):

    write_serializer_class = ProfileConfirmSerializer
    read_serializer_class = ProfileReadSerializer

    permission_classes = [
        HasAPIKey
    ]

    @use_transaction(lookup_url_kwarg='transaction_id')
    def create(self, request, *args, **kwargs):
        request.data.update(self.transaction.data)
        return super().create(request, *args, **kwargs)


class ProfileDetailView(rw_generics.RetrieveUpdateDestroyAPIView):

    write_serializer_class = ProfileUpdateSerializer
    read_serializer_class = ProfileReadSerializer

    lookup_url_kwarg = 'profile_id'

    permission_classes = [
        IsAuthenticated,
        IsManager
    ]

    def get_object(self):
        profile_id = self.kwargs[self.lookup_url_kwarg]
        user = self.request.user
        try:
            return user.userprofiles.get(id=profile_id)
        except Profile.DoesNotExist:
            raise NotFound

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ProfileUnlockView(views.APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request, version, profile_id):
        request.data.update({'id': profile_id})
        serializer = ProfileUnlockSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, HTTP_200_OK)


class ProfileRolesView(views.APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, version):
        roles = [
            {'id': k, 'name': v} for k, v in sorted(Profile.ROLE)
            if k != Profile.ROLE.owner]
        return Response(roles, HTTP_200_OK)


class ProfileCurrentView(rw_generics.RetrieveUpdateAPIView):

    write_serializer_class = ProfileUpdateSerializer
    read_serializer_class = ProfileReadSerializer

    def get_object(self):
        return getattr(self.request.user, 'profile', None)
