from django.contrib import admin

from .models import Book, Author, Publisher
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display=(
        'name',
        'get_authors', 
        'inventory_number',
        'year_of_publication',
    )
#    fieldsets =

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Publisher)