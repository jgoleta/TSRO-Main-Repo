from django.db import models
from django.utils.timezone import now  

class DeliveryHistory(models.Model):
    petroleum_name = models.CharField(max_length=100)
    supplier = models.CharField(max_length=100)
    delivery_code = models.CharField(max_length=20, unique=True)
    date_deliver = models.DateField()
    total_volume = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.delivery_code} - {self.petroleum_name}"

    class Meta:
        verbose_name = "Delivery"
        verbose_name_plural = "Deliveries"
        ordering = ['-date_deliver']

class ProductTransaction(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    volume_liters = models.DecimalField(max_digits=10, decimal_places=3)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} pcs"
    
class FuelTransaction(models.Model):
    machine_number = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    liters = models.DecimalField(decimal_places=3, max_digits=10)
    price_per_liter = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Machine {self.machine_number} - {self.fuel_type} - {self.amount}"

    class Meta:
        ordering = ['-created_at']

class ProductStock(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} units"

    class Meta:
        ordering = ['name']
    
