from django.shortcuts import render
from .models import LibraryUser, BookTransaction
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

def dashboard(request):
    
    # get and paginate library users
    library_users = LibraryUser.objects.all()
    users_page_number = request.GET.get('library_users_page')
    users_paginator = Paginator(library_users, '5')
    paginated_users = users_paginator.get_page(users_page_number)

    # get and paginate book transactions
    book_transactions = BookTransaction.objects.filter(date_due__lt=timezone.now())
    transactions_page_number = request.GET.get('transactions_page')
    transactions_paginator = Paginator(book_transactions, '5')
    paginated_book_transactions = transactions_paginator.get_page(transactions_page_number)

    context_object = {'library_users': paginated_users, 'book_transactions': paginated_book_transactions}

    return render(request, template_name='main/dashboard.html', context=context_object)