from autoslug import AutoSlugField

from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
        Класс описывает таблицу и поля в базе данных для сущности Category
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # slug = models.SlugField(allow_unicode=True, default='', blank=True)
    slug = AutoSlugField(
        populate_from='title',
        always_update=True,
        unique=True,
        null=True
    )

    class Meta:
        verbose_name = _('category')  # отображение названия модели в админке
        verbose_name_plural = _('categories')  # во множественном числе
        ordering = ('title',)  # сортировка по title (в алфавитном порядке)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:category-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class Tag(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
        Класс описывает таблицу и поля в базе данных для сущности Product
    """
    title = models.CharField(
        verbose_name='название',
        max_length=255,
        help_text='Максимальная длина 255 символов',
    )
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name='теги',
        blank=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='product',
        blank=True,
        null=True,
    )
    price = models.FloatField(
        verbose_name='цена',
    )
    discount = models.FloatField(
        verbose_name='скидка',
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
        ],
        default=0,
    )
    bonus = models.PositiveIntegerField(
        verbose_name='бонус',
        default=1,
    )
    in_stock = models.BooleanField(
        verbose_name='в наличии?',
        default=True,
    )

    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='дата последнего изменения',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('-pk',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product-detail', kwargs={
            'slug_category': self.category.slug,
            'pk': self.pk
        })

    @property
    def actual_price(self):
        return round(self.price * (1 - self.discount / 100), 2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Contacts(models.Model):
    title = models.CharField(max_length=128)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'title': 'Shop',
                'address': 'Kharkiv, some street',
                'phone': '0661234567'
            }
        )
        return obj


class ContactUs(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'contact us'
