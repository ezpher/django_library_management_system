from django.shortcuts import render
from .models import LibraryUser, BookTransaction
from django.utils import timezone

# Create your views here.

def dashboard(request):

    library_users = LibraryUser.objects.all()
    book_transactions = BookTransaction.objects.filter(date_due__lt=timezone.now())

    context_object = {'library_users': library_users, 'book_transactions': book_transactions}

    return render(request, template_name='main/dashboard.html', context=context_object)