from rest_framework_api_key.permissions import HasAPIKey

from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


class TokenObtainPairView(TokenObtainPairView):

    permission_classes = [
        HasAPIKey
    ]


class TokenRefreshView(TokenRefreshView):

    permission_classes = [
        HasAPIKey
    ]
