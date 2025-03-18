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
        queryset = User.objects.all_actives().order_by("-created_date")
        return queryset

    def get_serializer_class(self):

        if self.action in ["create", "update", "partial_update"]:
            return UserInputSerializer
        elif self.action in ["retrieve", "current_user"]:
            return UserDetailSerializer
        else:
            return UserSerializer

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
