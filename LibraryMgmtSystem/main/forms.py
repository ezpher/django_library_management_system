from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from .models import CustomUser, LibraryUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class LibraryUserEditForm(forms.ModelForm):

    card_no = forms.CharField(label='Card No.:', widget = forms.TextInput(attrs={'readonly':'readonly', 'class': 'field_readonly'}))
    name = forms.CharField(label='Name', widget = forms.TextInput(attrs={'required': True}))
    date_joined = forms.DateTimeField(label='Date Joined', widget = forms.TextInput(attrs={'readonly':'readonly', 'class': 'field_readonly'}))

    class Meta:
        model = LibraryUser
        fields = ('card_no', 'name', 'date_joined')