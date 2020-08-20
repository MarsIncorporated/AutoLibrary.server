from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models
import booksOperations

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    def number_of_instances(self):
        return self.bookinstance_set.count()
    number_of_instances.short_description = "Количество экземпляров"
    
    def isbn_plus_name(self):
        '''
        returns the book's isbn plus name; isbn is bordered in HTML
        '''
        
        return mark_safe(f'<span style="border: medium double #447e9b">{self.isbn:13d}</span> — {self.name}')
    isbn_plus_name.short_description = 'ISBN — название'
    isbn_plus_name.admin_order_field = 'name'
    
    search_fields = ['name', 'authors', 'subject__name',
                     'grade', 'isbn', 'inventory_number']
    
    list_display=(
        isbn_plus_name,
        'isbn',
        'authors', 
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

@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status',)
    readonly_fields = ('status',)
    fields = ('status', 'id', 'book')
    inlines = (booksOperations.admin.BookTakingInline,)
