from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, LibraryUser, Book, Author, Category, BookTransaction, Transaction

# custom user admin

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


# inline models for showing intermediary model widget in each of the connected tables

class BookTransactionInline(admin.TabularInline):
    model = BookTransaction
    extra = 1

class BookAdmin(admin.ModelAdmin):
    inlines = (BookTransactionInline,)

class TransactionAdmin(admin.ModelAdmin):
    inlines = (BookTransactionInline,)

# registrations
# TODO: add placeholders for certain fields e.g. transaction_ref

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(LibraryUser)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book, BookAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(BookTransaction)



