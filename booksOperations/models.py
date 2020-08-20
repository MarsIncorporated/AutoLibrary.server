from django.db import models
from datetime import timedelta
from django.utils import timezone

from django.conf import settings

import booksRecord, readersRecord


class BookTaking(models.Model):
    '''
    Модель описывает акты взятия книг.
    '''
    
    is_returned = models.BooleanField(
        default=False,
        verbose_name='возвращена?'
    )
    
    is_returned.boolean = True
    
    
    book_instance = models.ForeignKey(
        booksRecord.models.BookInstance,
        on_delete=models.CASCADE,
        editable=False,
        limit_choices_to={'status': booksRecord.models.BookInstance.IN_STORAGE},
        verbose_name="экземпляр книги",
    )
    
    student = models.ForeignKey(
        readersRecord.models.Student,
        on_delete=models.CASCADE,
        verbose_name="ученик"
    )
    
    when_taken = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name="Дата и время взятия"
    )
    
    when_returned = models.DateTimeField(
        default=timezone.now() + timedelta(
          days=settings.READERSRECORD_DEFAULT_TAKING_PERIOD),
        verbose_name="Дата и время возврата"
    )
    
    
    def save(self, *args, **kwargs):
        if not self.is_returned:
            self.book_instance.status = booksRecord.BookInstance.ON_HANDS
        else:
            self.book_instance.status = booksRecord.BookInstance.IN_STORAGE
        
        self.book_instance.save()           
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return str(self.book_instance)
    
    class Meta:
        indexes = (models.Index(fields=('is_returned',)),)
        get_latest_by = "when_taken"
        ordering = ['is_returned', "when_taken"]
        verbose_name_plural = 'акты взятия книг'
        verbose_name = 'акт взятия книги'
