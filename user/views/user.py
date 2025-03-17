from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# drf
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# from core.mixins import ApiErrorsMixin
from user.serializers import (
    UserSerializer,
    UserDetailSerializer,
    UserInputSerializer,
    UserDetailWithWalletSerializer,
)

# from user.permissions import IsOwnerOrReadOnly, IsUserObj

User = get_user_model()


class UserViewSetApi(
    viewsets.ModelViewSet,
):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk=None):
        instance = get_object_or_404(User, id=pk)
        return instance

    def get_queryset(self):
        queryset = User.all_active.business_layer().order_by("-created_date")
        return queryset

    def list(self, request):

        serializer = UserSerializer(
            self.get_queryset(), many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = UserDetailSerializer(
            instance=instance,
            context={"request": request},
        )
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = UserInputSerializer(
            instance=instance, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(
        detail=False,
        methods=["get"],
        name="get current user details",
        # url_path = 'buildings/rooms/(?P<pk>[^/.]+)',
    )
    def current_user(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            serializer = UserDetailSerializer(
                user,
                context={"request": request},
            )
            return Response(serializer.data)

        return Response(status="401")

    @action(
        detail=True,
        methods=["get"],
        name="user full detail",
        # url_path = 'buildings/rooms/(?P<pk>[^/.]+)',
    )
    def full_content(self, request, pk=None):
        user = self.get_object(pk=pk)
        serializer = UserDetailWithWalletSerializer(
            user,
            context={"request": request},
        )
        return Response(serializer.data)

        # def get_permissions(self):

    #     """Set custom permissions for each action."""
    #     if self.action == 'retrieve':
    #         self.permission_classes = [IsUserObj, ]
    #     elif self.action == 'list':
    #         self.permission_classes = [IsAdminUser, ]
    #     return super().get_permissions()
