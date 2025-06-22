from django.contrib import admin
from .models import DeliveryHistory, ProductTransaction, FuelTransaction

@admin.register(DeliveryHistory)
class DeliveryHistoryAdmin(admin.ModelAdmin):
    list_display = ('delivery_code', 'petroleum_name', 'supplier', 'date_deliver', 'total_volume', 'total_price', 'created_at')
    list_filter = ('supplier', 'date_deliver', 'petroleum_name')
    search_fields = ('delivery_code', 'petroleum_name', 'supplier')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date_deliver',)

@admin.register(ProductTransaction)
class ProductTransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'volume_liters', 'price_per_unit', 'total_price', 'created_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(FuelTransaction)
class FuelTransactionAdmin(admin.ModelAdmin):
    list_display = ('machine_number', 'fuel_type', 'amount', 'liters', 'price_per_liter', 'created_at')
    list_filter = ('machine_number', 'fuel_type', 'created_at')
    search_fields = ('fuel_type',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

