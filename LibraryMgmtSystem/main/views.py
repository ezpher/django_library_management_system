from django.shortcuts import render
from .models import LibraryUser, BookTransaction
from django.utils import timezone
from django.core.paginator import Paginator
from .filters import LibraryUserFilter

# Create your views here.

def dashboard(request):
    
    # get library users 
    library_users = LibraryUser.objects.all()

    # setup paginator
    users_page_number = 1
    paginated_users = None
    users_paginator = Paginator(library_users, '5')

    # setup filter
    library_user_filter = LibraryUserFilter(request.GET, queryset=library_users)

    # paginate library users 
    # Note: pagination will not work if name is not empty since it will always default to default pagination i.e. without search term
    if request.method == 'GET' and not request.GET.get('name', False):      
        users_page_number = request.GET.get('library_users_page')
        paginated_users = users_paginator.get_page(users_page_number)
    elif request.method == 'GET' and request.GET.get('name', False):
        library_users = library_user_filter.qs
        users_paginator = Paginator(library_users, '5')
        paginated_users = users_paginator.get_page(users_page_number)

    # get and paginate book transactions
    book_transactions = BookTransaction.objects.filter(date_due__lt=timezone.now())
    transactions_page_number = request.GET.get('transactions_page')
    transactions_paginator = Paginator(book_transactions, '5')
    paginated_book_transactions = transactions_paginator.get_page(transactions_page_number)

    context_object = {'library_user_filter': library_user_filter, 'library_users': paginated_users, 'book_transactions': paginated_book_transactions}

    return render(request, template_name='main/dashboard.html', context=context_object)