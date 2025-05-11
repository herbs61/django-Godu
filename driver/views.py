from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DriverForm
from .models import Driver

# Create your views here.

def index(request):
    drivers = Driver.objects.filter(user=request.user, is_deleted=0).order_by('-created_at')
    return render(request, 'driver/modules/driver/index.html')


def create(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES)
        if form.is_valid():
            driver = form.save(commit=False)
            driver.user = request.user  # Assuming you have a user field in your Driver model
            driver.save()
            messages.success(request, "Driver registered successfully.")
            return redirect('driver')  # Redirect to the driver's dashboard or any other page
        else:
            messages.error(request, "Error in form submission. Please correct the errors.")
    else:
        form = DriverForm()
    
    return render(request, 'driver/modules/driver/modals/add.html', {'form': form})