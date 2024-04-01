from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access") or None
        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {"refresh": str(refresh), "access": str(refresh.access_token)}
