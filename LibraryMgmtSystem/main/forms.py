from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from .models import CustomUser, LibraryUser, Book, Transaction, BookTransaction
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class LibraryUserCreateForm(forms.ModelForm):
    
    ''' should not have an initial date_joined created since will only take effect at time of form save'''
    # def __init__(self, *args, **kwargs):
    #     super(LibraryUserCreateForm, self).__init__(*args, **kwargs)
    #     self.fields['date_joined'].initial = timezone.now
    
    card_no = forms.CharField(label='Card No.:')    
    name = forms.CharField(label='Name')
    # date_joined = forms.DateTimeField(label='Date Joined', widget = forms.TextInput(attrs={'readonly':'readonly', 'class': 'field_readonly'}))

    class Meta:
        model = LibraryUser
        fields = ('card_no', 'name') # , date_joined

class LibraryUserEditForm(forms.ModelForm):

    card_no = forms.CharField(label='Card No.:', widget = forms.TextInput(attrs={'readonly':'readonly', 'class': 'field_readonly'}))
    name = forms.CharField(label='Name', widget = forms.TextInput(attrs={'required': True}))
    date_joined = forms.DateTimeField(label='Date Joined', widget = forms.TextInput(attrs={'readonly':'readonly', 'class': 'field_readonly'}))

    class Meta:
        model = LibraryUser
        fields = ('card_no', 'name', 'date_joined')


# Use multiple forms when checking out a book i.e. TransactionForm, and BookTransactionForm
# Book transaction form should also take in the selected library user from UI

class TransactionForm(forms.ModelForm):

    transaction_ref = forms.CharField(label='Transaction Ref.:', widget = forms.TextInput(attrs={'readonly':'readonly', 'class': 'field_readonly'}), min_length=17, max_length=17)

    class Meta:
        model = Transaction
        fields = ('transaction_ref',)

class BookTransactionForm(forms.ModelForm):

    book = forms.ModelChoiceField(label='Book:', queryset=Book.objects.all())

    class Meta:
        model = BookTransaction
        fields = ('book',)
