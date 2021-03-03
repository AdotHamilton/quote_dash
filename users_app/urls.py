from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.success),
    path('quotes/submit', views.addQuote),
    path('quotes/like/<int:id>', views.likeQuote),
    path('quotes/delete/<int:id>', views.deleteQuote),
    path('user/<int:id>', views.displayUserPage),
    path('myaccount/<int:id>', views.displayMyAccount),
    path('myaccount/update/<int:id>', views.updateAccount),
]