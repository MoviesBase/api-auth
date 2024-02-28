from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserModel

# flake8: noqa: E501


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            ('Personal Info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'second_last_name',
                    'email',
                )
            },
        ),
        (
            ('Permissions'),
            {'fields': ('is_active', 'is_admin', 'groups', 'is_staff')},
        ),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'username',
                    'email',
                    'password1',
                    'password2',
                    'first_name',
                    'last_name',
                    'second_last_name',
                ),
            },
        ),
    )


admin.site.register(UserModel, UserAdmin)
