from django.db import models

import core.models

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
        verbose_name="Заметки")
    
    grade = models.CharField(
        max_length=3,
        choices=core.models.GRADES,
        verbose_name="класс",
        help_text="номер и литера класса"
    )
    
    class Meta(core.models.Human.Meta):
        verbose_name = "ученик"
        verbose_name_plural = 'ученики'