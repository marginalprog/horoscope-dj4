from django.contrib import admin
from django.urls import path
from . import views  # импорт из той же папки представлений

urlpatterns = [
    # - параметр <sign_zodiac> передаётся в функцию и в ней обрабатывается
    #   это сделано для избавления от избыточности в файлах и загромождения кода.
    # - конвертеры роутов (путей) int\str, перенаправляющие запросы в зав-ти от инпута.
    path('type/', views.get_all_types),
    path('<int:month>/<int:day>/', views.get_info_by_day),
    path('type/<str:type_zodiac>/', views.get_info_about_type, name="type_name"),
    path('<int:sign_zodiac>/', views.get_info_about_sign_zodiac_number),
    path('<str:sign_zodiac>/', views.get_info_about_sign_zodiac, name="horoscope_name"),
    # - name - аргумент для reverse urls. Он помогает ф-ии reverse выстроить нужный путь к ресурсу из
    #   главного urls-файла проекта. Теперь не нужно переписывать весь код при изменении названия страницы, достаточно
    #   его(path) изменить в главном файле представлений views
    path('', views.index),
]
