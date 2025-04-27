from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BaseAuthentication

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
          access_token = request.COOKIES.get("access_token")
          if not access_token:
               return None
          jwt_auth = JWTAuthentication()
          validated_token = jwt_auth.get_validated_token(access_token)
          user = jwt_auth.get_user(validated_token)
          if not user or not user.is_active:
               return None
          return user, validated_token

