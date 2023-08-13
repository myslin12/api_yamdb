from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (get_jwt_token, register, GenreViewSet,
                    CategoryViewSet, TitleViewSet, UserViewSet)
from reviews.views import CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='title-review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment-review'
)
router.register(r"users", UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token')
]
