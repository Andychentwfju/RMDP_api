from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls, name='index'),
    path('driver/', include('driver.urls'), name='index'),
    path('restaurant/', include('restaurant.urls'), name='index'),
    path('order/', include('order.urls'), name='index'),
    path('menu/', include('menu.urls'), name='index'),
    path('geolocation/', include('geolocation.urls'), name='index'),
]
