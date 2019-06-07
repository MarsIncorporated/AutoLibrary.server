from django.contrib import admin

from .models import Book, Author, Publisher
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display=('name', 'get_authors', 'year_of_publishing')
#    fieldsets =

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Publisher)