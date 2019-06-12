from django.db import models
import barcodenumber
from django.core.exceptions import ValidationError

import core.models

def ean13_validator(value):
    if not barcodenumber.check_code(
        'ean13',
        str(value)
    ):
        raise ValidationError(
            'контрольная сумма штрихкода "%(value)s" неверна, проверьте введённые данные',
            params={'value':value}
        )

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
        validators=[ean13_validator],
        verbose_name='ISBN код',
        help_text='''ISBN код книги, \
указанный на штрих-коде сзади, уникален для каждого издания''',
    )
    
    name = models.CharField(
        max_length=65, 
        db_index=True, 
        unique=True, 
        verbose_name="название",
        help_text = 'Официальное название книги'
    )
    
    authors = models.ManyToManyField(
        'Author',
        verbose_name="автор(-ы)",
        help_text='''Автор или авторы книги, \
ссылается на :Model:`booksRecord.Author`'''
    )
    
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.PROTECT,
        db_index=False,
        verbose_name='издательство'
    )
    
    year_of_publication = models.SmallIntegerField(
        verbose_name="год издания"
    )
    
    edition = models.SmallIntegerField(
        verbose_name='номер издания'
    )
    
    publication_city = models.CharField(
        max_length=30,
        verbose_name="город издания",
        help_text='город издания книги, без "г. "'
    )
    
    inventory_number = models.SmallIntegerField(
        verbose_name='инвентарный номер',
        help_text='инвентарный номер из Книги Учёта' #надо уточнить
    )
    
    def get_authors(self):
        '''
        выдает список авторов книги через запятую
        '''
        
        return ', '.join((
            str(i) for i in self.authors.all()
        ))
    get_authors.short_description = "автор(-ы)"
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']
        verbose_name = 'книга'
        verbose_name_plural = 'книги'

class Author(core.models.Human):
    '''
    Модель описывает всех авторов книг в библиотеке,
    Ф.И.О. заполняется полностью.\n
    Правильно:\n
    \tФамилия:\tПушкин\n
    \tИмя:\tАлександр\n
    \tОтчество:\tСергеевич\n
    Неправильно:\n
    \tФамилия:\tПушкин\n
    \tИмя:\tА.\n
    \tОтчество:\tС.\n
    Для записи иностранных авторов 
    использовать кириллицу, отчество
    можно не указывать.\n
    Правильно:\n
    \tФамилия:\tЛондон\n
    \tИмя:\tДжек\n
    \tОтчество:\t\n
    Неправильно:\n
    \tФамилия:\tLondon\n
    \tИмя:\tJack\n
    \tОтчество:\tGriffith
    '''
       
    class Meta(core.models.Human.Meta):
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

class Publisher(models.Model):
    '''
    Модель описывает каждое издательство,
    в название не надо писать форму собственности
    предприятием (слова "ООО", "ПАО"), а также само
    слово "Издательство".\n
    Правильно:\n
    \tНаименование:\tЭксмо\n
    Неправильно:\n
    \t Наименование:\tООО "Издательство "Эксмо"
    '''
    name = models.CharField(
        max_length=65, 
        db_index=True, 
        unique=True, 
        verbose_name="наименование",
        help_text='''Официальное наименование 
издательства, без слов "Издательство", "ООО", "ПАО" и т. п.'''
    )
    
    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['name']
        verbose_name = 'издательство'
        verbose_name_plural = 'издательства'


class BookInstance(models.Model):
    '''
    Описывает каждую книгу в библиотеке,
    каждый экземпляр.
    '''
    
    id = models.PositiveIntegerField(
        primary_key=True,
        unique=True,
        verbose_name="индивидуальный идентификатор",
        help_text='''идентификатор книги, уникальный для \
каждого экземпляра; совпадает с номером на наклейке со штрихкодом'''
    )
    
    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        verbose_name="книга",
        help_text='''ссылка на модель Книга \
:Model:`booksRecord.Book`'''
    )