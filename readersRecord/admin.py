from django.contrib import admin

from .models import Student
import booksOperations.admin

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "grade")
    search_fields = ("second_name", 'first_name')
    inlines = (booksOperations.admin.BookTakingInline,)
