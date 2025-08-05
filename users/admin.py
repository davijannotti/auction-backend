from django.contrib import admin
from django import forms
from .models import User


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    search_fields = ("username", "email", "first_name", "last_name")
