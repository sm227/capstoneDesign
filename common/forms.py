from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from .models import Memo


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class MemoForm(forms.ModelForm):
    text = forms.CharField(label="메모 내용", widget=forms.Textarea(attrs={'rows': 3}))

    # time = forms.CharField(label="시간", max_length=50)  # 시간은 클라이언트에서 생성하여 전달해야 함

    class Meta:
        model = Memo
        fields = ['text']


class UserForm2(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('email', 'username', 'password')