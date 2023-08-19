from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title, User

from .filters import TitleFilter
from .mixins import ListCreateDestroyMixin
from .permissions import GenresTitlesPermission, IsAdmin
from .filters import UserFilter
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    SignupSerializer,
    TitleCreateSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)
    http_method_names = ('get', 'post', 'patch', 'delete')
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PATCH":
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    confirmation_code = default_token_generator.make_token(user)
    user.code = confirmation_code
    user.save()

    send_mail(
        subject="YaMDb registration",
        message=f"Your confirmation code: {confirmation_code}",
        from_email='dimam2311@gmai.com',
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )

    confirmation_code = serializer.validated_data.get("confirmation_code")
    if user.code == confirmation_code:
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(
        {"detail": "Invalid confirmation code."},
        status=status.HTTP_400_BAD_REQUEST
    )


class GenreViewSet(ListCreateDestroyMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (GenresTitlesPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateSerializer
        return TitleSerializer
