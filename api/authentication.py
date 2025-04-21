# /home/bmn/projects/label_app/label_api/api/authentication.py
import logging # Use logging for better practice
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# Get an instance of a logger
logger = logging.getLogger(__name__)

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access_token")
        # refresh_token = request.COOKIES.get("refresh_token") # Refresh logic not implemented here yet
        if not access_token:
            return None # No access token cookie found

        jwt_auth = JWTAuthentication()

        try:
            logger.debug("Attempting JWT validation from cookie...")
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
            if not user or not user.is_active:
                 logger.warning(f"Authentication failed: User inactive or deleted (token sub: {validated_token.get('user_id')})")
                 # You might raise AuthenticationFailed here or let it return None depending on desired behavior
                 # raise AuthenticationFailed('User inactive or deleted.')
                 return None # Treat inactive user as not authenticated for this request

            logger.info(f"JWT authentication successful for user: {user.username}")
            return user, validated_token
        except InvalidToken as e:
             # Token is invalid (expired, malformed, signature wrong, etc.)
             logger.warning(f"InvalidToken error during JWT authentication: {e}")
             # Raise AuthenticationFailed to signal DRF about the failure
             raise AuthenticationFailed('Invalid or expired token provided.')
        except TokenError as e:
             # General token processing error
             logger.warning(f"TokenError during JWT authentication: {e}")
             raise AuthenticationFailed('Token processing error.')
        except AuthenticationFailed as e:
             # Catch potential AuthenticationFailed from get_user (e.g., user not found)
             logger.warning(f"AuthenticationFailed during user retrieval: {e}")
             raise e # Re-raise the original exception
        except Exception as e:
             # Catch any other unexpected exceptions during the process
             logger.error(f"Unexpected error during JWT authentication: {type(e).__name__} - {e}", exc_info=True)
             # It's often better to raise a generic AuthenticationFailed than expose internal errors
             raise AuthenticationFailed('An unexpected error occurred during authentication.')

