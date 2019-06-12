from django.db import models

class Human (models.Model):
    '''
    Абстрактная модель человека.
    Используется в TODO
    '''
    
    second_name = models.CharField(
        max_length=25,
        verbose_name='фамилия',
        blank=False,
        help_text='Фамилия кириллицей'
    )
    
    first_name = models.CharField(
        max_length=25,
        verbose_name='имя',
        blank=False,
        help_text='Имя кириллицей'
    )
    
    middle_name = models.CharField(
        max_length=25,
        verbose_name='отчество',
        blank=True,
        help_text='Отчество кириллицей, необязательно'
    )
    
    @property
    def full_name(self):
        '''
        Возвращает полную фамилию, имя и отчество\n
        Например: Пушкин Александр Сергеевич
        '''
        return ' '.join((
            self.second_name, 
            self.first_name, 
            self.middle_name
        ))
    
    @property
    def short_name(self):
        '''
        Возвращает фамилию и сокращённые имя и отчество.\n
        Например: Пушкин А. С.
        '''
        
        '''
        The if below is required
        because the Index out of bounds will be raised,
        if the person hasn't a middle_name (try do ''[0] + '.')
        '''
        
        if self.middle_name:
            name_tuple = (
                self.second_name,
                self.first_name[0] + '.',
                self.middle_name[0] + '.'
            )
        else:
            name_tuple = (
                self.second_name,
                self.first_name[0] + '.',
            )
        
        return ' '.join(name_tuple)
    
    def __str__(self):
       return self.short_name
       
    class Meta:
        abstract = True
        ordering = ['second_name','first_name','middle_name']