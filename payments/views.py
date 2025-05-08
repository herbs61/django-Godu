from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from django.contrib import messages
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from paystackapi.transaction import Transaction
from django.conf import settings
import requests
import uuid

# Create your views here.
@login_required
def payment(request):
    payments = Payment.objects.filter(user=request.user, is_deleted=0).order_by('-created_at')
    return render(request, 'payment/modules/payment/index.html', {'payments': payments})


@login_required 
def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.reference = f'PAY-{uuid.uuid4().hex[:10].upper()}'
            payment.status = 'pending'  # You may update this after real processing
             # Generate transaction ID
            last_payment = Payment.objects.aggregate(last_id=Max('id'))['last_id'] or 0
            next_id = last_payment + 1
            payment.transaction_id = f'TRANS{next_id:04d}'  # Pads to 4 digits

            payment.save()
            
             # Check if the user selected Mobile Money or Credit Card
            if payment.payment_method in ['credit_card', 'mobile']:
                # Initialize Paystack transaction
                paystack = Transaction(api_key=settings.PAYSTACK_SECRET_KEY)
                response = paystack.initialize(
                    email=request.user.email,
                    amount=int(payment.amount * 100),  # Paystack expects the amount in kobo (smallest unit)
                    reference=payment.reference,
                    callback_url = f"{settings.SITE_URL}/payments/callback",  # Your callback URL
                )

                if response['status']:
                    payment.paystack_reference = response['data']['reference']
                    payment.save()  # Save Paystack reference to the payment record
                    # Redirect the user to Paystack's payment page
                    return redirect(response['data']['authorization_url'])

                messages.error(request, "An error occurred while initializing payment.")
                return redirect('payment')
            else:
                # Handle other payment methods like PayPal, Bank Transfer, etc.
                messages.info(request, "You selected a different payment method. Proceed with other steps.")
                return redirect('payment')
    else:
        form = PaymentForm()
    return render(request, 'payment/modules/payment/modals/add.html', {'form': form})


@csrf_exempt
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, "No payment reference found.")
        return redirect('payment')

    # Verify the payment using Paystack's API
    paystack = Transaction(api_key=settings.PAYSTACK_SECRET_KEY)
    response = paystack.verify(reference)

    if response['status']:
        payment_data = response['data']
        if payment_data['status'] == 'success':
            # Update payment status to 'completed'
            try:
                payment = Payment.objects.get(reference=reference)
                payment.payment_status = 'completed'
                payment.save()
                messages.success(request, "Payment successful.")
                return redirect('payment')
            except Payment.DoesNotExist:
                messages.error(request, "Payment record not found.")
                return redirect('payment')
    
    messages.error(request, "Payment failed or was unsuccessful.")
    return redirect('payment')



@login_required
def edit(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment updated successfully.")
            return redirect('payment')
    return redirect('payment')


@login_required
def delete(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user, is_deleted=0)
    if request.method == 'POST':
        payment.is_deleted = 1  # mark as soft-deleted using integer
        payment.save()
        messages.success(request, "Payment deleted successfully.")
    return redirect('payment')