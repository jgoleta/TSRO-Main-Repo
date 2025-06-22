from django import forms
from .models import DeliveryHistory, ProductTransaction, FuelTransaction

class DeliveryForm(forms.ModelForm):
    supplier = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': 'required',
            'placeholder': 'Enter supplier name'
        })
    )

    class Meta:
        model = DeliveryHistory
        fields = ['petroleum_name', 'supplier', 'delivery_code', 'date_deliver', 'total_volume', 'total_price']
        widgets = {
            'date_deliver': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'date-deliver'
            }),
            'delivery_code': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'delivery-code',
                'readonly': 'readonly'
            }),
            'petroleum_name': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'total_volume': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'step': '0.01'
            }),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'step': '0.01'
            })
        }

class ProductTransactionForm(forms.ModelForm):
    class Meta:
        model = ProductTransaction
        fields = ['name', 'quantity', 'volume_liters', 'price_per_unit', 'total_price']

class FuelTransactionForm(forms.ModelForm):
    class Meta:
        model = FuelTransaction
        fields = ['machine_number', 'fuel_type', 'amount', 'liters', 'price_per_liter']
        widgets = {
            'machine_number': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'fuel_type': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'step': '0.01'}),
            'liters': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'step': '0.001'}),
            'price_per_liter': forms.NumberInput(attrs={'class': 'form-control', 'required': True, 'step': '0.01'}),
        }