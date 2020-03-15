from django.contrib import admin

from . import models

@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    def number_of_instances(self):
        return self.bookinstance_set.count()
    number_of_instances.short_description = "Количество экземпляров"
    
    search_fields = ['name', 'authors__second_name', 'subject__name',
                     'grade', 'isbn', 'inventory_number']
    
    list_display=(
        'name',
        'get_authors', 
        'inventory_number',
        number_of_instances,
    )
    
    autocomplete_fields = ['authors', 'publisher', 'subject']
    
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
    
    search_fields = ['second_name', 'first_name']
    
    list_display = (
        '__str__',
        number_of_books
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

@admin.register(models.Publisher)
class PublisherAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(models.TakenBook)
class TakenBookAdmin(admin.ModelAdmin):
    list_display = ('book_instance', 'is_returned',
      'student', 'when_taken', 'when_returned',)
    
    readonly_fields = ('when_taken', 'book_instance')
    
    fieldsets = (
      (None, {'fields': ('is_returned', 'book_instance', 'student')}),
      (None, {'fields': ('when_taken', 'when_returned')}),
    )
