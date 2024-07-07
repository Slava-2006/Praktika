from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main),
    path('advanced_search/', views.advanced_search, name='advanced_search'),
    path('search_history/', views.search_history, name='search_history'),
    path('vacancies/<int:search_query_id>/', views.vacancies_by_search_query, name='vacancies_by_search_query'),

]