from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if password:
            from django.core.exceptions import ValidationError
            from django.contrib.auth.password_validation import validate_password

            try:
                validate_password(password, self.instance)
            except ValidationError as e:
                raise forms.ValidationError(e.messages)
        return password


class FeedbackForm(forms.Form):
    # nome = forms.CharField(
    #     max_length=100,
    #     widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Seu Nome"})
    # )
    # email = forms.EmailField(
    #     widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Seu E-mail"})
    # )
    assunto = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Assunto"})
    )
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Escreva seu feedback..."})
    )
