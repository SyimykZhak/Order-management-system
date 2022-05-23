from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Products(models.Model):
    title = models.CharField("Название", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Фото", upload_to = "images/")
    price = models.PositiveIntegerField("Цена",)
    kol = models.PositiveIntegerField("Количество",)
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Продукты"
        verbose_name_plural = "Продукты"

class Order(models.Model):
    name = models.ForeignKey(Products, verbose_name="продукты",on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField("количество заказа",null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.update_at = timezone.now()
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer}-{self.name}'
    
    class Meta:
        verbose_name = "Заказы"
        verbose_name_plural = "Заказы"



    

