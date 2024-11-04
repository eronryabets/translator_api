import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from rest_framework.permissions import BasePermission
from translator_api.users import SimpleUser
import logging

logger = logging.getLogger(__name__)


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        logger.info("Начало аутентификации в JWTAuthentication")
        token = request.COOKIES.get('access_token')

        if not token:
            logger.info("Токен не найден в cookies, проверяем заголовок Authorization")
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header[7:]
                logger.info("Токен получен из заголовка Authorization")

        if not token:
            logger.warning("Токен не найден ни в cookies, ни в заголовке Authorization")
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            logger.info(f"Токен успешно декодирован: {payload}")
        except jwt.ExpiredSignatureError:
            logger.error("Ошибка аутентификации: срок действия токена истёк")
            raise AuthenticationFailed('Токен истёк')
        except jwt.InvalidTokenError:
            logger.error("Ошибка аутентификации: неверный токен")
            raise AuthenticationFailed('Неверный токен')

        user = SimpleUser(payload)
        logger.info(f"Пользователь успешно аутентифицирован: {user.id}")
        return (user, None)


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, что текущий пользователь является владельцем объекта
        return obj.user_id == request.user.id