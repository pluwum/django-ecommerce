from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', )

    def clean_password(self):
        password1 = self.clean_data.get("password1")
        password2 = self.clean_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords Did not match")
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password',
            'is_active',
            'is_merchant',
            'is_staff',
            'is_superuser',
        )

    def clean_password(self):
        return self.initial["password"]
