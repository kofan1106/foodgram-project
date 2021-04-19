from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
User = get_user_model()

class RegisterForm(ModelForm):
    name = forms.CharField(label=_('Имя'), max_length=100)
    username = forms.CharField(label=_('Имя пользователя'), max_length=100)
    email = forms.EmailField(
        label=_('Адрес электронной почты'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    password = forms.CharField(
        label=_('Пароль'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
