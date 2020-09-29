from django.db.models import Q

from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model

UserModel = get_user_model()


class AuthModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """ Аутентификация с помощью email/phone и password """
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            user = UserModel.objects.get(Q(email=username) | Q(phone=username))
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) \
                    and self.user_can_authenticate(user):
                return user
