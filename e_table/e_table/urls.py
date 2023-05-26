"""
URL configuration for e_table project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

import reservations.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('restaurants', reservations.views.restaurants_all),
    path('book/<int:restaurant_id>', reservations.views.book_table),
    path('reservations/upcoming', reservations.views.reservations_upcoming),
    path('reservations/past', reservations.views.reservations_past),
    path('reservations/cancel/<int:rid>', reservations.views.reservations_cancel),
    path('reservations/own', reservations.views.my_reservations),
    path('restaurants/own', reservations.views.my_restaurants),
    path('', reservations.views.home),
]
