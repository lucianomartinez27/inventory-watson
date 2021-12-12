from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('inventario', views.StockListView.as_view(), name='inventory'),
    path('nuevo', views.StockCreateView.as_view(), name='new-stock'),
    path('productos/<pk>/editar', views.StockUpdateView.as_view(), name='edit-stock'),
    path('productos/<pk>/eliminar', views.StockDeleteView.as_view(), name='delete-stock'),
    path('mesas-y-mozos', views.TablesAndWaitersView.as_view(), name='tables-and-waiters'),
    path('mesa/<pk>/eliminar', views.TableDeleteView.as_view(), name='delete-table'),
    path('mesa/<pk>/editar', views.TableUpdateView.as_view(), name='edit-table'),
    path('mozo/<pk>/eliminar', views.WaiterDeleteView.as_view(), name='delete-waiter'),
    path('mozo/<pk>/editar', views.WaiterUpdateView.as_view(), name='edit-waiter'),
    path('nueva-mesa', views.TableCreateView.as_view(), name='new-table'),
    path('nuevo-mozo', views.WaiterCreateView.as_view(), name='new-waiter'),
    
]