from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from cask.constants import (
    MAX_LENGTH_BARREL_MANUFACTURER,
    MAX_LENGTH_TYPE_OF_OAK,
    MAX_NAME_CASK,
    MIN_VALUE_FILLING_BARREL,
    MAX_VALUE_FILLING_BARREL,
    MIN_VOLUME_VALUE,
    MAX_VOLUME_VALUE,
)

User = get_user_model()


class Cask(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_NAME_CASK,
    )
    owner = models.ManyToManyField(
        User,
        related_name='casks',
        verbose_name='Владелец',
        through='CaskOwner',
    )
    volume_in_liters = models.PositiveIntegerField(
        verbose_name='Объем в литрах',
        validators=(MinValueValidator(limit_value=MIN_VOLUME_VALUE),
                    MaxValueValidator(limit_value=MAX_VOLUME_VALUE)),
    )
    description = models.TextField(
        verbose_name='Описание/Примечание',
    )
    start_of_operation = models.DateField(
        verbose_name='Начало эксплуатации',
    )
    type_of_oak = models.ForeignKey(
        'TypeOfOak',
        related_name='casks',
        verbose_name='Тип древесины',
        on_delete=models.CASCADE
    )
    barrel_manufacturer = models.CharField(
        verbose_name='Производитель бочки',
        max_length=MAX_LENGTH_BARREL_MANUFACTURER,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='casks/',
        null=True,
        blank=True
    )
    new_or_old = models.BooleanField(
        verbose_name='Новая или б/у',
    )


class TypeOfOak(models.Model):
    name = models.CharField(
        verbose_name='Тип древесины',
        max_length=MAX_LENGTH_TYPE_OF_OAK,
    )


class CaskOwner(models.Model):
    cask = models.ForeignKey(
        Cask,
        related_name='owners',
        verbose_name=Cask,
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(  # Точно так? Не удалиться бочка, если удалить одного из владельцев?
        User,
        related_name='casks',
        verbose_name='Владелец',
        on_delete=models.CASCADE
    )


class FillingBarrel(models.Model):
    cask = models.ForeignKey(  # Точно ли каскад? Не удалиться бочка, если удалить залив?
        Cask,
        related_name='filling_barrels',
        verbose_name=Cask,
        on_delete=models.CASCADE
    )
    number_of_filling_barrel = models.PositiveIntegerField(
        verbose_name='Номер залива бочки',
        validators=(MinValueValidator(limit_value=MIN_VALUE_FILLING_BARREL),
                    MaxValueValidator(limit_value=MAX_VALUE_FILLING_BARREL)),
    )
    volume_filling_in_liters = models.PositiveIntegerField(
        verbose_name='Объем в литрах',
        validators=(MinValueValidator(limit_value=MIN_VOLUME_VALUE),
                    MaxValueValidator(limit_value=MAX_VOLUME_VALUE)),
    )
    filling_drink = models.DateField(
        verbose_name='Дата залива напитка',
    )
    draing_drink = models.DateField(
        verbose_name='Дата слива напитка',
    )
    initial_alcohol_content = models.FloatField(  # Точно тут?
        verbose_name='Начальное содержание алкоголя',
    )
    final_alcohol_content = models.FloatField(  # Точно тут?
        verbose_name='Конечное содержание алкоголя',
    )

    def __str__(self):
        return f'{self.cask} - {self.number_of_filling_barrel}'