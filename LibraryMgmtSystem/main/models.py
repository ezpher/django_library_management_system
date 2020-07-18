from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager
from django.contrib.auth import get_user_model
from django.utils import timezone
from _datetime import timedelta

# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class LibraryUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, null=True)
    name = models.TextField()
    card_no = models.CharField(max_length=12)
    date_joined = models.DateTimeField(default=timezone.now) # note that if field is indicated as non-editable e.g. auto_now_add=True, cannot render on forms such as your admin forms/regular django forms

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    CATEGORIES = (
        ("Biography", "Biography"),
        ("Fantasy", "Fantasy"),
        ("Mystery", "Mystery"),
        ("Romance", "Romance"),
        ("Sci-Fi", "Sci-Fi"),
        ("Self-Help", "Self-Help"),
        ("Thriller", "Thriller")                
    )

    category_name = models.CharField(max_length=20, choices=CATEGORIES, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

class Book(models.Model):
    title = models.TextField()
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    stock = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Transaction(models.Model):
    transaction_ref = models.CharField(max_length=13, unique=True)
    books = models.ManyToManyField(Book, through='BookTransaction')
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.transaction_ref

def get_default_duedate():
    return timezone.now().date() + timedelta(days=7)

class BookTransaction(models.Model):
    library_user = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, related_name='book_transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='book_transactions')

    date_due = models.DateField(default=get_default_duedate)
    date_returned = models.DateField(null=True, blank=True)
    times_renewed = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


    



    

