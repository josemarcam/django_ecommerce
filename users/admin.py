from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from users.forms import UserCreationForm, UserChangeForm
from users.models import User

# Register your models here.
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
