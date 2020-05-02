from django.contrib import admin
from .models import Book, BookInstance, Visitor, Registration, User

#admin.site.register(Book)
#admin.site.register(BookInstance)
admin.site.register(Visitor)
admin.site.register(Registration)
admin.site.register(User)


class BookInstanceInline(admin.TabularInline):
    model = BookInstance


class BookAdmin(admin.ModelAdmin):
    inlines = [
        BookInstanceInline,
    ]


admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance)
