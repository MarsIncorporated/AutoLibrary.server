from django.db import models

# Create your models here.

class Book (models.Model):
    '''
    Модель описывает любые книги в хранилище, будь то
    учебники или художественную литературу.
    Если книги имеют одинаковые наименования,
    но разные года, то они считаются <b>разными</b>.
    Здесь хранится не каждый экземпляр книги, а только их описания.
    К примеру, в хранилище есть 100 книг <i>Алгебра. 7 класс</i>, 
    при этом в этой модели <u>хранится ТОЛЬКО ОДНА запись</u>.
    '''
    # the comment above ↑ is to automatically generate a documentation
    # You should write such comments for everything you make.
    # Read more here: https://docs.djangoproject.com/en/2.2/ref/contrib/admin/admindocs/
    
    name = models.CharField(
        max_length=65, 
        db_index=True, 
        unique = True, 
        verbose_name="Наименование",
        help_text = 'Официальное наименование книги'
    )
    annotation = models.TextField( #not sure that it's needed
        max_length=200, 
        verbose_name="Аннотация", 
        blank=True,
        help_text='''Аннотация книги, \
взятая с обратной стороны титульного листа. \
Желательна к заполнению.'''
        # the text above is needed to generate a documentation
    )
    author = models.ManyToManyField(
        'author',
        verbose_name = "Автор(-ы)",
        help_text = '''Автор или авторы книги, \
ссылается на :Model:`booksRecord.Author`'''
    )
    
    def __str__(self):
        return self.name

class Author (models.Model):
    '''
    Модель описывает всех авторов книг в библиотеке,
    Ф.И.О. заполняется полностью.\n
    <i style="color: lime">Правильно: Пушкин Александр Сергеевич</i>
    <i style="color: red">Неправильно: Пушкин А. С.</i>
    Используется в :Model:`booksRecord.Book`.
    Для иностранных авторов отчество можно не писать,
    поля заполнять кириллицей, например:
    <i>Джек Лондон</i>
    '''
    
    first_name = models.CharField(
        max_length=25,
        verbose_name='Имя',
    )
    middle_name = models.CharField(
        max_length=25,
        verbose_name='Отчество'
    )
    second_name = models.CharField(
        max_length=25,
        verbose_name='Фамилия'
    )
    
    def __str__():
       return 
        
    def get_full_name(self):
        return ' '.join((
            self.second_name, 
            self.first_name, 
            self.middle_name
        ))
     
    def get_short_name(self):
        return ' '.join((
            self.second_name,
            self.first_name[0] + '.',
            [self.middle_name[0] + '.', None] [self.middle_name]
        ))