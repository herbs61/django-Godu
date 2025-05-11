from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            'license_no', 'license_type', 'license_expiry',
            'gh_card', 'gh_expiry', 'reg_code',
            'fname', 'mname', 'lname', 'dob', 'gender',
            'phone', 'whatsapp', 'email', 'years_experience',
            'account_type', 'account_name', 'account_number', 'residence',
            'medical', 'passport', 'hometown',
            'guarantor_no', 'guarantor_name', 'guarantor_residence',
            'guarantor_no2', 'guarantor_name2', 'guarantor_residence2',
            'emergency_name', 'emergency_no', 'emergency_residence', 'emergency_email',
            'emergency_name2', 'emergency_no2', 'emergency_residence2', 'emergency_email2',
            'contract_dura'
                  ]
        
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date'}),
            'gh_expiry': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }