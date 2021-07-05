from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from LibraryProject import settings

User = get_user_model()

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Person(BaseModel):
    TYPE_OF_USER = (
        ('Staff', 'Staff'),
        ('Reader', 'Reader'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=0)
    email = models.EmailField(unique=True)
    type_of_user = models.CharField(max_length=20, default="Reader", choices=TYPE_OF_USER)

    def __str__(self):
        return self.email


class Book(BaseModel):
    title = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to='book_images/', null=True)
    author = models.CharField(max_length=30)
    date_published = models.DateField()
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, null=True)

    def __str__(self):
        return self.title


class Comment(BaseModel):
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='comments')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=100)

    def __str__(self):
        return self.text


class Like(BaseModel):
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, related_name='likes')
    liked = models.ForeignKey(User, related_name='users', blank=True, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['book_name', 'liked']]




class Category(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    book_name = models.ManyToManyField(Book,related_name='categories',through='Book_Category')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Book_Category(BaseModel):
    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['book_name','category_name']]

    def __str__(self):
        return f'{self.book_name}'