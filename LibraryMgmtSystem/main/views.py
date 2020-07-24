from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from .decorators import is_authorised_user
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.utils import timezone
from django.core.paginator import Paginator

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, FormView
from .models import LibraryUser, BookTransaction
from .forms import LibraryUserEditForm, LibraryUserCreateForm, CustomUserCreationForm
from .filters import LibraryUserFilter

# Create your views here.

@is_authorised_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        custom_user = authenticate(request, username=username, password=password)

        if custom_user is not None and custom_user.is_staff:
            login(request, custom_user)
            return redirect('dashboard')
        elif custom_user is not None and not custom_user.is_staff:            	
            messages.warning(request, 'User does not have admin privileges')
        else:
            messages.warning(request, 'Username OR Password is incorrect')

        '''somehow checking groups is not reliable'''
        # group = None

        # if custom_user is not None and custom_user.groups.exists():
        #     group = custom_user.groups.all()[0].name
        #     if group == 'admin':
        #         login(request, custom_user)
        #         return redirect('dashboard')
        #     else:            	
        #         messages.warning(request, 'User does not have admin privileges')
        # else:
        #     messages.warning(request, 'Username OR Password is incorrect')
            
    context = {}
    return render(request, template_name='main/login.html', context=context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):

    # get book status fields: total books on loan, books_not_yet_overdue, books_due
    total_books_on_loan = BookTransaction.objects.filter(date_returned__isnull=True).count()
    books_not_yet_overdue = BookTransaction.objects.filter(date_returned__isnull=True).filter(date_due__gt=timezone.now()).count()
    books_due = BookTransaction.objects.filter(date_returned__isnull=True).filter(date_due__lt=timezone.now()).count()
    
    # get library users and count
    library_users = LibraryUser.objects.all().order_by('name')
    library_users_count = library_users.count()

    # setup paginator
    users_page_number = 1
    paginated_users = None
    users_paginator = Paginator(library_users, '5')

    # setup filter
    library_user_filter = LibraryUserFilter(request.GET, queryset=library_users)

    # paginate library users 
    # Note: pagination will not work if name is not empty and reloading page without clicking search button since it will always default to default pagination i.e. without search term
    if request.method == 'GET' and not request.GET.get('name', False):      
        users_page_number = request.GET.get('library_users_page')
        paginated_users = users_paginator.get_page(users_page_number)
    elif request.method == 'GET' and request.GET.get('name', False):
        library_users = library_user_filter.qs
        users_paginator = Paginator(library_users, '5')
        paginated_users = users_paginator.get_page(users_page_number)

    # get and paginate book transactions
    book_transactions = BookTransaction.objects.filter(date_due__lt=timezone.now()).order_by('date_due')
    transactions_page_number = request.GET.get('transactions_page')
    transactions_paginator = Paginator(book_transactions, '5')
    paginated_book_transactions = transactions_paginator.get_page(transactions_page_number)

    context_object = {'total_books_on_loan': total_books_on_loan, 'books_not_yet_overdue': books_not_yet_overdue, 'books_due': books_due, 'library_user_filter': library_user_filter, 'library_users': paginated_users, 'library_users_count': library_users_count, 'book_transactions': paginated_book_transactions}

    return render(request, template_name='main/dashboard.html', context=context_object)

class LibraryUserList(ListView):

    template_name = 'main/library_users.html'
    # default context_object_name is the model object in lowercase e.g. libraryuser
    # if dealing with list of objects, default context_object_name is object_list
    # use context_object_name to override default name in both cases
    context_object_name = 'library_users'

    def get_queryset(self):
        # get library users
        library_users = get_list_or_404(LibraryUser.objects.all().order_by('name'))

        # setup paginator
        users_page_number = 1
        paginated_users = None
        users_paginator = Paginator(library_users, '5')        

        # differentiate between clicking on page number and loading page for first time
        if self.request.method == 'GET' and self.request.GET.get('library_users_page'):      
            users_page_number = self.request.GET.get('library_users_page')
            paginated_users = users_paginator.get_page(users_page_number)
        elif self.request.method == 'GET' and not self.request.GET.get('library_users_page', False):
            paginated_users = users_paginator.get_page(users_page_number)

        # return paginated library users        
        return paginated_users

class LibraryUserDetails(DetailView):

    template_name = 'main/library_user_view.html'
    context_object_name = 'library_user'

    # use get_queryset even when trying to retrieve single object
    def get_queryset(self):
        self.library_user = get_object_or_404(LibraryUser, id=self.kwargs['pk'])
        return LibraryUser.objects.filter(id=self.library_user.id)

class LibraryUserUpdate(UpdateView):

    template_name = 'main/library_user_update.html'
    form_class = LibraryUserEditForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_queryset(self):
        self.library_user = get_object_or_404(LibraryUser, id=self.kwargs['pk'])
        return LibraryUser.objects.filter(id=self.library_user.id)

    def get_success_url(self):
        return reverse('library_user_update', kwargs = {'pk': self.kwargs['pk']}) 

class LibraryUserCreate(FormView):

    template_name = 'main/library_user_create.html'

    def get(self, request, *args, **kwargs):
        base_user_creation_form = CustomUserCreationForm()
        base_user_creation_form.prefix = 'user_create_form'

        library_user_creation_form = LibraryUserCreateForm()
        library_user_creation_form.prefix = 'library_user_create_form'
        return render(request, template_name=self.template_name, context={'user_create_form':base_user_creation_form, 'library_user_create_form':library_user_creation_form})

    def post(self, request, *args, **kwargs):
        base_user_creation_form = CustomUserCreationForm(self.request.POST, prefix='user_create_form')
        library_user_creation_form = LibraryUserCreateForm(self.request.POST, prefix='library_user_create_form')

        if base_user_creation_form.is_valid() and library_user_creation_form.is_valid():            
            new_user = base_user_creation_form.save()
            new_library_user = library_user_creation_form.save(commit=False) 
            new_library_user.user = new_user
            new_library_user.save()
            return HttpResponseRedirect(reverse('library_user_view', args=(new_library_user.pk,)))
        else:
            return self.form_invalid(request, base_user_creation_form, library_user_creation_form, **kwargs)

    def form_invalid(self, request, base_user_creation_form, library_user_creation_form, **kwargs):
        base_user_creation_form.prefix='user_create_form'
        library_user_creation_form.prefix='library_user_create_form'
        return render(request, template_name=self.template_name, context={'user_create_form':base_user_creation_form, 'library_user_create_form':library_user_creation_form})



