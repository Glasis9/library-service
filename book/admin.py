from django.contrib import admin

from book.models import Book


# class TicketInline(admin.TabularInline):
#     model = Book
#     extra = 1
#
#
# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     inlines = (TicketInline,)
#

admin.site.register(Book)
