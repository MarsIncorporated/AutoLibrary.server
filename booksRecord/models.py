from django.db import models
from django.conf import settings
from django.utils import timezone

from datetime import timedelta

import core.models
import readersRecord
from . import validators


class Book(models.Model):
    '''
    Модель описывает любые книги в хранилище, будь то
    учебники или художественную литературу.
    Если книги имеют одинаковые наименования,
    но разные года, то они считаются разными.\n
    Здесь хранится не каждый экземпляр книги, а только их описания.
    К примеру, в хранилище есть 100 книг «Алгебра. 7 класс», 
    при этом в этой модели хранится ТОЛЬКО ОДНА запись.
    '''
    
    # The comment above ↑ is to automatically generate a documentation.
    # You should write such comments for everything you make.
    # Read more here: https://docs.djangoproject.com/en/2.2/ref/contrib/admin/admindocs/
    
    isbn = models.BigIntegerField(
        unique=True,
        primary_key=True,
        validators=[validators.ean13_validator],
        verbose_name='ISBN код',
        help_text='''ISBN код книги, \
указанный на штрих-коде сзади, уникален для каждого издания''',
    )
    
    name = models.CharField(
        max_length=65, 
        verbose_name="название",
        help_text = 'Официальное название книги'
    )
    
    authors = models.CharField(
        verbose_name="автор(-ы)",
        max_length=200
    )
    
    year_of_publication = models.SmallIntegerField(
        verbose_name="год издания"
    )
    
    publisher = models.CharField(
        verbose_name='издательство',
        max_length=20
    )
    
    edition = models.SmallIntegerField(
        verbose_name='номер издания'
    )
    
    publication_city = models.CharField(
        max_length=30,
        verbose_name="город издания",
        help_text='город издания книги, без "г. "'
    )
    
    grade = models.CharField(
        max_length=5,
        verbose_name="класс",
        blank=True,
        help_text='''Для учебных книг. Может быть диапазоном, к примеру: \
«Физика. Задачник. 7-9 класс»''',
        validators=[validators.grade_validator]
    )
    
    subject = models.CharField(
        verbose_name="предмет",
        max_length=20, 
        blank=True,
        null=True
    )
    
    inventory_number = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name='инвентарный номер',
        help_text='инвентарный номер из Книги Учёта' #should be specified
    )
    
    def __str__(self):
        return self.name
        
    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=['inventory_number']),
            models.Index(fields=["grade", "subject"])
        ]
        
        ordering = ['name']
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

class BookInstance(models.Model):
    '''
    Описывает каждую книгу в библиотеке,
    каждый экземпляр.
    '''
    
    IN_STORAGE = 0
    ON_HANDS = 1
    EXPIRED = 2
    WRITTEN_OFF = 3
    
    STATUSES = (
        (IN_STORAGE, "в хранилище"),
        (ON_HANDS, "на руках"),
        (EXPIRED, "истёк срок возврата"),
        (WRITTEN_OFF, "снята с учёта")
    )
    
    status = models.PositiveSmallIntegerField(
        choices=STATUSES,
        editable=False,
        default=IN_STORAGE,
        verbose_name="статус"
    )
    
    id = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        verbose_name="ID",
        validators=[validators.ean8_validator],
        help_text='''идентификатор книги, уникальный для \
каждого экземпляра; совпадает с номером штрихкода на наклейке'''
    )
    
    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        db_index=False,
        verbose_name="книга",
        help_text='''ссылка на модель Книга \
:Model:`booksRecord.Book`'''
    )
    
    def __str__(self):
        return str(self.book)
    
    class Meta:
        ordering = ["id"]
        indexes = (models.Index(fields=('status',)),)
        verbose_name = "экземпляр книги"
        verbose_name_plural = "экземпляры книг"


class TakenBook(models.Model):
    '''
    Модель описывает взятые экземпляры книг.
    '''
    
    is_returned = models.BooleanField(
        default=False,
        verbose_name='возвращена?'
    )
    
    is_returned.boolean = True
    
    
    book_instance = models.ForeignKey(
        'BookInstance',
        on_delete=models.CASCADE,
        editable=False,
        limit_choices_to={'status': BookInstance.IN_STORAGE},
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
            self.book_instance.status = BookInstance.ON_HANDS
        else:
            self.book_instance.status = BookInstance.IN_STORAGE
        
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
