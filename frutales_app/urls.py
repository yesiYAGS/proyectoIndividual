from django.urls import path
from frutales_app import views

urlpatterns = [
    path('', views.home),
    path('home-user', views.homeUser),
    path('login', views.login),
    path('logout', views.logout),
    path('create', views.createUser),
    path('carrusel', views.carrusel),
    path('producto/<str:nombre>',views.producto),
    path('addtocart',views.addtocart),
    
]