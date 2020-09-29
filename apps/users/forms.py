from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'email', 'phone', 'name', 'surname', 'password1', 'password2'
        )
