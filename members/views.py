from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import DeliveryHistory, ProductTransaction, FuelTransaction, ProductStock
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from django.core.serializers.json import DjangoJSONEncoder
from .forms import ProductTransactionForm


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")


@login_required(login_url='login')
def homepage(request):
    return render(request, "homepage.html")


@login_required
def fuel_view(request):
    try:
        # Get all transactions ordered by machine number and creation date
        transactions = FuelTransaction.objects.all().order_by('machine_number', 'created_at')
        print(f"Debug: Found {len(transactions)} transactions")
        
        # Group transactions by machine and fuel type
        transactions_by_machine = {}
        for transaction in transactions:
            machine_key = f'machine_{transaction.machine_number}'
            if machine_key not in transactions_by_machine:
                transactions_by_machine[machine_key] = {
                    'unleaded': [],
                    'diesel': []
                }
            
            # Convert fuel type to lowercase for consistent comparison
            fuel_type = transaction.fuel_type.lower()
            transaction_data = {
                'amount': float(transaction.amount),
                'liters': float(transaction.liters),
                'price_per_liter': float(transaction.price_per_liter),
                'created_at': transaction.created_at
            }
            
            if fuel_type == 'unleaded':
                transactions_by_machine[machine_key]['unleaded'].append(transaction_data)
            elif fuel_type == 'diesel':
                transactions_by_machine[machine_key]['diesel'].append(transaction_data)
        
        print(f"Debug: Grouped transactions: {transactions_by_machine}")
        
        # Convert transactions to JSON for JavaScript
        transactions_json = json.dumps(list(transactions.values()), cls=DjangoJSONEncoder)
        
        return render(request, 'fuel.html', {
            'transactions_by_machine': transactions_by_machine,
            'transactions': transactions_json,
            'debug_count': len(transactions)
        })
    except Exception as e:
        print(f"Error in fuel_view: {str(e)}")
        return render(request, 'fuel.html', {
            'transactions_by_machine': {},
            'transactions': '[]',
            'debug_count': 0
        })


@login_required(login_url='login')
def history_view(request):
    return render(request, "history.html")


@login_required(login_url='login')
def product_view(request):
    if request.method == 'POST':
        form = ProductTransactionForm(request.POST)
        if form.is_valid():
            # Get the product stock
            product_name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']
            
            try:
                stock = ProductStock.objects.get(name=product_name)
                if stock.quantity >= quantity:
                    # Create transaction
                    transaction = form.save()
                    
                    # Update stock
                    stock.quantity -= quantity
                    stock.save()
                    
                    messages.success(request, 'Transaction added successfully!')
                else:
                    messages.error(request, f'Not enough stock available. Only {stock.quantity} units left.')
            except ProductStock.DoesNotExist:
                messages.error(request, 'Product not found in stock.')
    else:
        form = ProductTransactionForm()
    
    # Get all transactions and stock
    transactions = ProductTransaction.objects.all().order_by('-created_at')
    stock_items = ProductStock.objects.all()
    
    # Calculate totals
    total_quantity = sum(t.quantity for t in transactions)
    total_amount = sum(t.total_price for t in transactions)
    
    context = {
        'form': form,
        'transactions': transactions,
        'stock_items': stock_items,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    }
    return render(request, "product.html", context)


@login_required(login_url='login')
def sales_view(request):
    # Get transactions with timezone awareness
    fuel_transactions = FuelTransaction.objects.all().order_by('-created_at')
    product_transactions = ProductTransaction.objects.all().order_by('-created_at')
    
    # Add debug logging
    print(f"Debug: Number of fuel transactions: {len(fuel_transactions)}")
    for transaction in fuel_transactions:
        print(f"Debug: Transaction - Machine: {transaction.machine_number}, "
              f"Type: {transaction.fuel_type}, Amount: {transaction.amount}, "
              f"Liters: {transaction.liters}, Price: {transaction.price_per_liter}, "
              f"Date: {transaction.created_at}")
    
    context = {
        'fuel_transactions': fuel_transactions,
        'product_transactions': product_transactions
    }
    return render(request, "sales.html", context)


def logout_view(request):
    logout(request)
    return redirect("login")


def webpage6(request):
    if request.method == 'POST':
        try:
            # Get form data
            petroleum_name = request.POST.get('petroleum_name')
            supplier = request.POST.get('supplier')
            delivery_code = request.POST.get('delivery_code')
            date_deliver = request.POST.get('date_deliver')
            total_volume = request.POST.get('total_volume')
            total_price = request.POST.get('total_price')

            # Create new delivery record
            delivery = DeliveryHistory(
                petroleum_name=petroleum_name,
                supplier=supplier,
                delivery_code=delivery_code,
                date_deliver=date_deliver,
                total_volume=total_volume,
                total_price=total_price
            )
            delivery.save()
            messages.success(request, 'Delivery record saved successfully!')
            return redirect('webpage6')
        except Exception as e:
            messages.error(request, f'Error saving delivery record: {str(e)}')
            return redirect('webpage6')

    # Get all delivery records
    deliveries = DeliveryHistory.objects.all().order_by('-date_deliver')
    return render(request, 'history.html', {'deliveries': deliveries})


def delete_delivery(request, delivery_id):
    if request.method == 'POST':
        delivery = get_object_or_404(DeliveryHistory, id=delivery_id)
        delivery.delete()
        messages.success(request, 'Delivery record deleted successfully!')
    return redirect('webpage6')


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


@login_required(login_url='login')
@csrf_exempt
@require_http_methods(["POST"])
def save_fuel_transaction(request):
    try:
        data = json.loads(request.body)
        transaction = FuelTransaction(
            machine_number=data['machine_number'],
            fuel_type=data['fuel_type'],
            amount=data['amount'],
            liters=data['liters'],
            price_per_liter=data['price_per_liter']
        )
        transaction.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required(login_url='login')
@csrf_exempt
@require_http_methods(["POST"])
def delete_fuel_transaction(request):
    if request.method == 'POST':
        try:
            # Debug logging
            print("Debug: Delete request received")
            print("Debug: POST data:", request.POST)
            
            # Get the transaction ID from the form
            transaction_id = request.POST.get('transaction_id')
            print(f"Debug: Attempting to delete transaction ID: {transaction_id}")
            
            # Find and delete the transaction
            transaction = FuelTransaction.objects.get(id=transaction_id)
            if transaction:
                transaction.delete()
                print("Debug: Transaction deleted successfully")
                messages.success(request, 'Transaction deleted successfully!')
            else:
                print("Debug: Transaction not found")
                messages.error(request, 'Transaction not found')
                
        except FuelTransaction.DoesNotExist:
            print("Debug: Transaction does not exist")
            messages.error(request, 'Transaction not found')
        except Exception as e:
            print(f"Debug: Error deleting transaction: {str(e)}")
            messages.error(request, f'Error deleting transaction: {str(e)}')
    
    return redirect('webpage6')


@login_required(login_url='login')
def add_product_stock(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        
        if name and quantity:
            try:
                quantity = int(quantity)
                if quantity > 0:
                    stock, created = ProductStock.objects.get_or_create(name=name)
                    if not created:
                        stock.quantity += quantity
                    else:
                        stock.quantity = quantity
                    stock.save()
                    messages.success(request, f'Stock updated for {name}')
                else:
                    messages.error(request, 'Quantity must be greater than 0')
            except ValueError:
                messages.error(request, 'Invalid quantity')
        else:
            messages.error(request, 'Please provide both name and quantity')
    
    return redirect('webpage5')


@login_required(login_url='login')
def delete_product(request, product_id):
    if request.method == 'POST':
        try:
            transaction = ProductTransaction.objects.get(id=product_id)
            # Return the quantity to stock
            stock = ProductStock.objects.get(name=transaction.name)
            stock.quantity += transaction.quantity
            stock.save()
            # Delete the transaction
            transaction.delete()
            messages.success(request, 'Transaction deleted successfully!')
        except ProductTransaction.DoesNotExist:
            messages.error(request, 'Transaction not found')
        except ProductStock.DoesNotExist:
            messages.error(request, 'Product stock not found')
    
    return redirect('webpage5')


@login_required(login_url='login')
def delete_product_stock(request, stock_id):
    if request.method == 'POST':
        stock = get_object_or_404(ProductStock, id=stock_id)
        stock.delete()
        messages.success(request, f'Product stock "{stock.name}" has been deleted.')
    return redirect('webpage5')
