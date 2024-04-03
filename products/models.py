from django.db import models
from django.contrib.auth.models import AbstractUser


class Type(models.Model):

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class NewUser(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(unique=True, max_length=200)
    type = models.ForeignKey("Type", blank=True, null=True, on_delete=models.PROTECT)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"email: {self.email}, type: {self.type}"

    class Meta:
        ordering = ("-id",)


class Status(models.Model):

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Section(models.Model):

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=220)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.CharField(max_length=660)
    category = models.CharField(max_length=220)
    image = models.CharField(max_length=220)
    status = models.ForeignKey("Status", blank=True, null=True, on_delete=models.PROTECT)
    sections = models.ManyToManyField(Section)
    owner = models.ForeignKey('NewUser', related_name='products', on_delete=models.CASCADE)