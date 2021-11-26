from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.StockListView.as_view(), name='inventory'),
    path('nuevo', views.StockCreateView.as_view(), name='new-stock'),
    path('agregar-categoria', views.CategoryCreateView.as_view(), name='new-category'),
    path('stock/<pk>/editar', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/eliminar', views.StockDeleteView.as_view(), name='delete-stock'),
]