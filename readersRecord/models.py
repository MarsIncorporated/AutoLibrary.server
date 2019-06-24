from django.db import models

import core

class Student(core.models.Human):
    '''
    Модель описывает ученика.
    Предполагается, что модель будет
    заполняться при помощи файла вывода
    кнопки "Экспорт в Moodle".
    '''
    
    id = models.PositiveIntegerField(
        unique=True,
        primary_key=True,
        verbose_name="индивидуальный идентификатор",
    )
    
    notes = models.TextField(
        max_length=500,
        verbose_name="Заметки"
    )
    
    grade = models.CharField(
        max_length=3,
        choices=core.GRADES,
        verbose_name="класс",
        help_text="номер и литера класса"
    )
    
    first_lang = models.CharField(
        max_length=2,
        choices=core.LANGUAGES,
        verbose_name='Первый язык',
        blank=True,
    )
    
    second_lang = models.CharField(
        max_length=2,
        choices=core.LANGUAGES,
        verbose_name='Второй язык',
        blank=True,
    )
    
    class Meta(core.models.Human.Meta):
        ordering = ['id']
        
        verbose_name = "ученик"
        verbose_name_plural = 'ученики'