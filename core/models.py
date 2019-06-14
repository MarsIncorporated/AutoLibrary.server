from django.db import models

GRADES = (('1 классы', (('1А', '1 «А»'), ('1Б', '1 «Б»'), ('1В', '1 «В»'), ('1Г', '1 «Г»'), ('1Д', '1 «Д»'), ('1Е', '1 «Е»'))), ('2 классы', (('2А', '2 «А»'), ('2Б', '2 «Б»'), ('2В', '2 «В»'), ('2Г', '2 «Г»'), ('2Д', '2 «Д»'), ('2Е', '2 «Е»'))), ('3 классы', (('3А', '3 «А»'), ('3Б', '3 «Б»'), ('3В', '3 «В»'), ('3Г', '3 «Г»'), ('3Д', '3 «Д»'), ('3Е', '3 «Е»'))), ('4 классы', (('4А', '4 «А»'), ('4Б', '4 «Б»'), ('4В', '4 «В»'), ('4Г', '4 «Г»'), ('4Д', '4 «Д»'), ('4Е', '4 «Е»'))), ('5 классы', (('5А', '5 «А»'), ('5Б', '5 «Б»'), ('5В', '5 «В»'), ('5Г', '5 «Г»'), ('5Д', '5 «Д»'), ('5Е', '5 «Е»'))), ('6 классы', (('6А', '6 «А»'), ('6Б', '6 «Б»'), ('6В', '6 «В»'), ('6Г', '6 «Г»'), ('6Д', '6 «Д»'), ('6Е', '6 «Е»'))), ('7 классы', (('7А', '7 «А»'), ('7Б', '7 «Б»'), ('7В', '7 «В»'), ('7Г', '7 «Г»'), ('7Д', '7 «Д»'), ('7Е', '7 «Е»'))), ('8 классы', (('8А', '8 «А»'), ('8Б', '8 «Б»'), ('8В', '8 «В»'), ('8Г', '8 «Г»'), ('8Д', '8 «Д»'), ('8Е', '8 «Е»'))), ('9 классы', (('9А', '9 «А»'), ('9Б', '9 «Б»'), ('9В', '9 «В»'), ('9Г', '9 «Г»'), ('9Д', '9 «Д»'), ('9Е', '9 «Е»'))), ('10 классы', (('10А', '10 «А»'), ('10Б', '10 «Б»'), ('10В', '10 «В»'), ('10Г', '10 «Г»'), ('10Д', '10 «Д»'), ('10Е', '10 «Е»'))), ('11 классы', (('11А', '11 «А»'), ('11Б', '11 «Б»'), ('11В', '11 «В»'), ('11Г', '11 «Г»'), ('11Д', '11 «Д»'), ('11Е', '11 «Е»'))))

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
        indexes = [
            models.Index(fields=[
                "second_name",
                "first_name"
            ])
        ]
        abstract = True
        ordering = [
            'second_name',
            'first_name',
            'middle_name'
        ]