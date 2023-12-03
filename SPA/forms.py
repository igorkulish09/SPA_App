from django import forms
from .models import Comment
# from captcha.fields import ReCaptchaField


class CommentForm(forms.ModelForm):
    # captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ['user_name', 'email', 'captcha', 'text',]
