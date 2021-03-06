"""Main App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name="logout"),
    path('', views.dashboard,  name='dashboard'),
    path('library_users/', views.LibraryUserList.as_view() ,name='library_users'),
    # note that object-identifer should use pk instead of user-defined parameter or else error will be thrown
    path('library_user/<int:pk>/', views.LibraryUserDetails.as_view() ,name='library_user_view'),
    path('library_user_create/', views.LibraryUserCreate.as_view(), name='library_user_create'),
    path('library_user_update/<int:pk>/', views.LibraryUserUpdate.as_view(), name='library_user_update'),
    path('library_user_delete/<int:pk>/', views.LibraryUserDelete.as_view(), name='library_user_delete'),
    path('checkin_book/<int:pk>/', views.CheckinBook.as_view(), name='checkin_book'),  
    path('checkout_book_view/', views.CheckoutBookView.as_view(), name='checkout_book_view'),   
    path('get_checkout_widget/<int:uid>/', views.CheckoutBookWidget.as_view(), name='checkout_book_widget'),   
]


