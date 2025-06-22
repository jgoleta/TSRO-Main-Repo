from django.contrib import admin
from django.urls import path
from advTSRO import index 
from members import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.webpage1, name='webpage1'),
    path('page2/', index.webpage2, name='webpage2'),
    path('page3/', index.webpage3, name='webpage3'),
    path('page4/', index.webpage4, name='webpage4'),
    path('page5/', views.product_view, name='webpage5'),
    path('page6/', views.sales_view, name='webpage6'),
    path('delete_delivery/<int:delivery_id>/', index.delete_delivery, name='delete_delivery'),
    path('delete_product/<int:product_id>/', index.delete_product, name='delete_product'),
    path('register/', index.register_view, name='register'),
    path('save_fuel_transaction/', views.save_fuel_transaction, name='save_fuel_transaction'),
    path('delete_fuel_transaction/', views.delete_fuel_transaction, name='delete_fuel_transaction'),
    path('add_product_stock/', views.add_product_stock, name='add_product_stock'),
    path('delete_product_stock/<int:stock_id>/', views.delete_product_stock, name='delete_product_stock'),
]
