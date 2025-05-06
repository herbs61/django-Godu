from .models import Member
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from .forms import UserRegistrationForm
from django.utils import timezone
import traceback
from django.contrib.auth.decorators import login_required

from django.contrib import messages


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                # Email activation
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                mail_subject = "Activate your account"
                message = render_to_string('users/auth/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                email_message = EmailMessage(
                    mail_subject, message, to=[user.email])
                email_message.content_subtype = 'html'

                email_sent = email_message.send()
                if email_sent:
                    user.save()
                    return render(request, 'users/auth/check_email.html')
                else:
                    messages.error(
                        request, "Failed to send verification email.")

            except Exception as e:
                print(traceback.format_exc())
                messages.error(request, "Error occurred. Please try again.")
        else:
            messages.error(request, "Invalid form. Please correct the errors.")
    else:
        form = UserRegistrationForm()

    return render(request, 'users/auth/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified_at = timezone.now()
        user.save()

        login(request, user)
        return redirect('dashboard')  # Redirect to login page after activation
    else:
        return HttpResponse('Activation link is invalid!')


def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, "users/auth/login.html")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_active or not user.email_verified_at:
                # Resend activation email
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)
                mail_subject = "Activate your account"
                message = render_to_string('users/auth/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                })
                email_message = EmailMessage(
                    mail_subject, message, to=[user.email])
                email_message.content_subtype = 'html'
                email_message.send()

                messages.info(
                    request, "Your email is not verified. We've sent you a new activation link.")
                return render(request, 'users/auth/check_email.html')

            login(request, user)
            # Change to your homepage or dashboard URL
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "users/auth/login.html")


def user_logout(request):
    logout(request)
    return redirect('login')


# Redirect to login page if not authenticated
@login_required(login_url='login')
def dashboard(request):
    return render(request, 'users/components/dashboard.html')
