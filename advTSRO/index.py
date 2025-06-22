from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from members.forms import DeliveryForm, ProductTransactionForm
from members.models import DeliveryHistory, ProductTransaction, FuelTransaction
from datetime import datetime


def webpage1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('webpage2')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
            
    return render(request, 'login.html')

def webpage2(request):
    return render(request, 'homepage.html')

def webpage3(request):
    fuel_transactions = FuelTransaction.objects.all().order_by('-created_at')
    product_transactions = ProductTransaction.objects.all().order_by('-created_at')

    return render(request, 'fuel.html', {
        'fuel_transactions': fuel_transactions,
        'product_transactions': product_transactions
    })

def webpage4(request):
    today = datetime.now().strftime('%Y%m%d')
    latest_delivery = DeliveryHistory.objects.filter(
        delivery_code__startswith=f'DLV{today}'
    ).order_by('-delivery_code').first()
    
    initial_data = {}
    if latest_delivery:
        try:
            last_number = int(latest_delivery.delivery_code.split('-')[1])
            new_number = last_number + 1
        except (IndexError, ValueError):
            new_number = 1
    else:
        new_number = 1
    
    initial_data['delivery_code'] = f'DLV{today}-{str(new_number).zfill(3)}'
    form = DeliveryForm(initial=initial_data)
    deliveries = DeliveryHistory.objects.all()

    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            try:
                delivery = form.save()
                messages.success(request, f'Delivery record saved successfully! Delivery Code: {delivery.delivery_code}')
                return redirect('webpage4')
            except Exception as e:
                messages.error(request, f'Error saving delivery: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, 'history.html', {
        'form': form,
        'deliveries': deliveries,
    })

def delete_delivery(request, delivery_id):
    if request.method == 'POST':
        delivery = get_object_or_404(DeliveryHistory, id=delivery_id)
        delivery.delete()
        messages.success(request, 'Delivery record deleted successfully!')
    return redirect('webpage4')

def webpage5(request):
    if request.method == 'POST':
        form = ProductTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product transaction saved!")
            return redirect('webpage5')
    else:
        form = ProductTransactionForm()

    transactions = ProductTransaction.objects.all().order_by('-created_at')
    
    # Calculate totals
    total_quantity = sum(transaction.quantity for transaction in transactions)
    total_amount = sum(transaction.total_price for transaction in transactions)
    
    return render(request, 'product.html', {
        'form': form,
        'transactions': transactions,
        'total_quantity': total_quantity,
        'total_amount': total_amount
    })

def delete_product(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(ProductTransaction, id=product_id)
        product.delete()
        messages.success(request, "Product deleted successfully.")
    return redirect('webpage5')

def webpage6(request):
    fuel_transactions = FuelTransaction.objects.all().order_by('-created_at')
    product_transactions = ProductTransaction.objects.all().order_by('-created_at')

    return render(request, 'sales.html', {
        'fuel_transactions': fuel_transactions,
        'product_transactions': product_transactions
    })


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("reg_username")
        email = request.POST.get("email")
        password = request.POST.get("reg_password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('webpage1')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('webpage1')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('webpage1')
        
        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Registration successful! Please login.")
            return redirect('webpage1')
        except Exception as e:
            messages.error(request, f"Error creating user: {str(e)}")
            return redirect('webpage1')
    
    return redirect('webpage1')
