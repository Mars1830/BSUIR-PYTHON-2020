from django.contrib import admin
from .models import Book, BookInstance, Visitor, Registration, User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
import logging
from .forms import SignUpForm

logger = logging.getLogger(__name__)

admin.site.register(Visitor)
admin.site.register(Registration)


class MyUserAdmin(UserAdmin):
    model = get_user_model()
    add_form = SignUpForm
    list_display = ('email', 'first_name', 'last_name', 'date_joined',
                    'is_active', 'is_staff', 'is_superuser', 'verified',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile',)}),
    )


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    inlines = [
        BookInstanceInline,
    ]


admin.site.register(User, MyUserAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance)
