from django.contrib import admin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm


admin.site.register(CustomUser, UserAdmin)
