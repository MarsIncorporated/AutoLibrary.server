from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


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

class TakenBookInline(admin.TabularInline):
    model = models.TakenBook
    readonly_fields = ('is_returned', 'student', 'when_taken', 'when_returned',)
    extra = 0
    can_delete = False

@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status',)
    readonly_fields = ('status',)
    fields = ('status', 'id', 'book')
    inlines = (TakenBookInline,)

@admin.register(models.TakenBook)
class TakenBookAdmin(admin.ModelAdmin):
    
    def book_instance_id_plus_name(self):
        '''
        returns the book's id plus name; id is bordered in HTML
        '''
        
        return mark_safe(f'<span style="border: thin solid #447e9b">{self.book_instance.id:08d}</span> — {self.book_instance}')
    book_instance_id_plus_name.short_description = "Экземпляр книги"
    book_instance_id_plus_name.admin_order_field = 'book_instance__book__name'
    

    list_display = (book_instance_id_plus_name, 'is_returned',
      'student', 'when_taken', 'when_returned',)
    
    readonly_fields = ('when_taken', 'book_instance')
    list_filter = ('is_returned',)
    
    fieldsets = (
      (None, {'fields': ('is_returned', 'book_instance', 'student')}),
      (None, {'fields': ('when_taken', 'when_returned')}),
    )
