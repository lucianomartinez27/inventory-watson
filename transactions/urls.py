from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('proveedores/', views.SupplierListView.as_view(), name='suppliers-list'),
    path('proveedores/nuevo', views.SupplierCreateView.as_view(), name='new-supplier'),
    path('proveedores/<pk>/editar', views.SupplierUpdateView.as_view(), name='edit-supplier'),
    path('proveedores/<pk>/eliminar', views.SupplierDeleteView.as_view(), name='delete-supplier'),
    path('proveedores/<name>', views.SupplierView.as_view(), name='supplier'),

    path('compras/', views.PurchaseView.as_view(), name='purchases-list'), 
    path('compras/nuevo', views.SelectSupplierView.as_view(), name='select-supplier'), 
    path('compras/nuevo/<pk>', views.PurchaseCreateView.as_view(), name='new-purchase'),    
    path('compras/<pk>/eliminar', views.PurchaseDeleteView.as_view(), name='delete-purchase'),
    
    path('ventas/', views.SaleView.as_view(), name='sales-list'),
    path('ventas/nuevo', views.SaleCreateView.as_view(), name='new-sale'),
    path('ventas/<pk>/eliminar', views.SaleDeleteView.as_view(), name='delete-sale'),

    path("compras/<billno>", views.PurchaseBillView.as_view(), name="purchase-bill"),
    path("ventas/<billno>", views.SaleBillView.as_view(), name="sale-bill"),
]