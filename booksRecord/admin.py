from django.contrib import admin

from .models import (
    Book, Author, Publisher,
    BookInstance, Subject,
    TakenBook
)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    def number_of_instances(self):
        return self.bookinstance_set.count()
    number_of_instances.short_description = "Количество экземпляров"
    
    list_display=(
        'name',
        'get_authors', 
        'inventory_number',
        number_of_instances,
    )
    
    fieldsets = (
      ("Идентификаторы", {'fields':
        ('isbn', 'inventory_number')
      }),
      
      ('Основная информация', {'fields':
        ('name', 'authors')
      }),
      
      ('Информация об издании', {'fields':
        ('publisher', 'publication_city',
         'year_of_publication', 'edition')
      }),
      
      ("Учебная информация", {'fields':
        ('grade', 'subject')
      }),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    def number_of_books(self):
        return self.book_set.count()
    number_of_books.short_description = 'количество книг'
    
    list_display = (
        '__str__',
        number_of_books
    )    


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status',)
    readonly_fields = ('status',)
    fields = ('status', 'id', 'book')

admin.site.register(Publisher)
admin.site.register(Subject)

@admin.register(TakenBook)
class TakenBookAdmin(admin.ModelAdmin):
    list_display = ('book_instance', 'is_returned',
      'student', 'when_taken', 'when_returned',)
    
    readonly_fields = ('when_taken', 'book_instance')  # the comma is required (to define a tuple)
    
    fieldsets = (
      (None, {'fields': ('is_returned', 'book_instance', 'student')}),
      (None, {'fields': ('when_taken', 'when_returned')}),
    )