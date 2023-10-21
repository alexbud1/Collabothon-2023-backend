from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = SimpleRouter()
router.register(r"signup", views.SignUpViewSet, basename="user_signup")
router.register(r"personal-info", views.PersonalInfoViewSet, basename="personal_info")
router.register(r"survey", views.SurveyViewSet, basename="survey")
router.register(r"message", views.MessageViewSet, basename="message")
router.register(r"mood", views.MoodViewSet, basename="mood")

appname = "api"

urlpatterns = router.urls + [
    path(r'refresh-login/', TokenRefreshView.as_view(), name='user_refresh_token_login'),
    path(r'login/', TokenObtainPairView.as_view(), name='user_credentials_login'),
]
