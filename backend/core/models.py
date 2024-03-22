from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q, F


class MyUser(AbstractUser):
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'


User = MyUser


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers',
        verbose_name='Пользователь'
    )
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions',
        verbose_name='Подписчик'
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'подписчики'
        constraints = [
            UniqueConstraint(
                fields=['user', 'follower'],
                name='unique_follower'),
            CheckConstraint(
                check=~Q(user=F('follower')),
                name="can't_sub_on_self"
            )
        ]
