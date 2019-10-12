from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('charge', views.charge, name='charge'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("menu", views.menu, name="menu"),
    path("basket",views.basket,name="basket"),
    path("ajax/basket/", views.ajax_basket,name="ajax_basket"),
    path("ajax/checkout/", views.ajax_checkout,name="ajax_checkout"),
]

# Urls for the webpage
