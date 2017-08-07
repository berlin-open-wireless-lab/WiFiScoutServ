from django.contrib.auth.forms import UserCreationForm

from captcha.fields import CaptchaField


class UserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('captcha', )
