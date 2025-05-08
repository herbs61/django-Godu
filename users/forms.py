from django import forms
from .models import Member
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='confirm_password', widget=forms.PasswordInput)

    class Meta:
        model = Member
        fields = ['fname', 'mname', 'lname', 'dob', 'gender', 'email']  
        # Removed 'roles'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.roles = 'user'  # Ensures it's always "user"
        if commit:
            user.save()
        return user


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['fname', 'mname', 'lname', 'dob', 'gender', 'email', 'profile_picture']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }