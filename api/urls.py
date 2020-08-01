from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"movies", views.MoviesViewSet)
router.register(r"ratings", views.RatingsViewSet, basename="ratings")
router.register(r"comments", views.CommentsViewSet, basename="comments")
router.register(r"movie/raport", views.RaportViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path("", include(router.urls,)),
    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

app_name = 'api'