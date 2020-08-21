from django.contrib import admin
from django.utils.safestring import mark_safe

from . import models


class BookTakingInline(admin.TabularInline):
    model = models.BookTaking
    readonly_fields = ('when_taken',)
    raw_id_fields = ('book_instance',)
    extra = 0
    can_delete = False

@admin.register(models.BookTaking)
class BookTakingAdmin(admin.ModelAdmin):
    
    def book_instance_id_plus_name(self):
        '''
        returns the book's id plus name; id is bordered in HTML
        '''
        
        return mark_safe(f'<span style="border: thin solid #447e9b">{self.book_instance.id:08d}</span> — {self.book_instance}')
    book_instance_id_plus_name.short_description = "Экземпляр книги"
    book_instance_id_plus_name.admin_order_field = 'book_instance__book__name'
    

    list_display = (book_instance_id_plus_name, 'is_returned',
      'student', 'when_taken', 'when_returned',)
    
    readonly_fields = ('when_taken',)
    list_filter = ('is_returned',)
    
    fieldsets = (
      (None, {'fields': ('is_returned', 'book_instance', 'student')}),
      (None, {'fields': ('when_taken', 'when_returned')}),
    )
