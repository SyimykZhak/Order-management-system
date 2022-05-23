from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    customer = models.OneToOneField(User,verbose_name="пользователь", on_delete=models.CASCADE)
    score = models.CharField("имя магазина",max_length=100)
    address = models.CharField("адрес",max_length=200)
    phone = models.CharField("телефон",max_length=50)
    image = models.ImageField("фото",upload_to='profile_images')

    def __str__(self):
        return f'{self.customer.username}'

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"