from django.urls import path, re_path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.IngredientListView.as_view(), name='inventory'),
    path('productos', views.StockListView.as_view(), name='product-list'),
    path('nuevo', views.StockCreateView.as_view(), name='new-stock'),
    path('agregar-categoria', views.CategoryCreateView.as_view(), name='new-category'),
    path('categoria/<pk>/eliminar', views.CategoryDeleteView.as_view(), name='delete-category'),
    path('ingredientes/<pk>/eliminar', views.IngredientDeleteView.as_view(), name='delete-ingredient'),
    path('ingredientes/<pk>/editar', views.IngredientUpdateView.as_view(), name='edit-ingredient'),
    path('productos/<pk>/editar', views.StockUpdateView.as_view(), name='edit-stock'),
    path('productos/<pk>/eliminar', views.StockDeleteView.as_view(), name='delete-stock'),
    path('mesas-y-mozos', views.TablesAndWaitersView.as_view(), name='tables-and-waiters'),
    path('mesa/<pk>/eliminar', views.TableDeleteView.as_view(), name='delete-table'),
    path('mesa/<pk>/editar', views.TableUpdateView.as_view(), name='edit-table'),
    path('mozo/<pk>/eliminar', views.WaiterDeleteView.as_view(), name='delete-waiter'),
    path('mozo/<pk>/editar', views.WaiterUpdateView.as_view(), name='edit-waiter'),
    path('ingrediente', views.IngredientCreateView.as_view(), name='add-ingredient'),

    path('nueva-mesa', views.TableCreateView.as_view(), name='new-table'),
    path('nuevo-mozo', views.WaiterCreateView.as_view(), name='new-waiter'),
    
]