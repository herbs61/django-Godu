from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method', 'description']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean_payment_method(self):
        payment_method = self.cleaned_data.get('payment_method')
        if payment_method not in dict(Payment.PAYMENT_METHOD_CHOICES).keys():
            raise forms.ValidationError("Invalid payment method selected.")
        return payment_method