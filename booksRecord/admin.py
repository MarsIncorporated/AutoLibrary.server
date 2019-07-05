from django.contrib import admin

from . import models

@admin.register(models.Book)
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

@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    def number_of_books(self):
        return self.book_set.count()
    number_of_books.short_description = 'количество книг'
    
    list_display = (
        '__str__',
        number_of_books
    )    

class TakenBookInline(admin.TabularInline):
    model = models.TakenBook
    readonly_fields = ('book_instance', 'student',
      'when_taken', 'when_returned')

@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'status',)
    readonly_fields = ('status',)
    fields = ('status', 'id', 'book')
    inline = (TakenBookInline)

admin.site.register(models.Publisher)
admin.site.register(models.Subject)

'''
@admin.register(models.TakenBook)
class TakenBookAdmin(admin.ModelAdmin):
    list_display = ('book_instance', 'is_returned',
      'student', 'when_taken', 'when_returned',)
    
    readonly_fields = ('when_taken', 'book_instance')
    
    fieldsets = (
      (None, {'fields': ('is_returned', 'book_instance', 'student')}),
      (None, {'fields': ('when_taken', 'when_returned')}),
    )
'''