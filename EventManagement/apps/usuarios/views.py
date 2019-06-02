from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import requests
from django.views.generic import ListView, DetailView 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from social_django.models import UserSocialAuth

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
        facebook_info = {}
        facebook_info["nombre"] = facebook_login.extra_data["name"]
        facebook_info["email"] = facebook_login.extra_data["email"]
        facebook_info["foto"] = facebook_login.extra_data["picture"]["data"]["url"]
        facebook_info["url_perfil"] = facebook_login.extra_data["profile_url"]
    except UserSocialAuth.DoesNotExist:
        facebook_info = None

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
        response = requests.get(
            'https://www.googleapis.com/oauth2/v1/userinfo?alt=json',
            params={'access_token': google_login.extra_data['access_token']}
        ).json()
        print("--------------")
        print(response)
        print("--------------")
        google_info = {}
        google_info["nombre"] = response["name"]
        google_info["email"] = response["email"]
        google_info["foto"] = response["picture"]
        google_info["url_perfil"] = response["link"]
    except UserSocialAuth.DoesNotExist:
        google_info = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'settings.html', {
        'facebook_info': facebook_info,
        'google_info': google_info,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})

class MixinAdministrador(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.perfil.rol == Perfil.ADMINISTRADOR

class UsuariosListar(MixinAdministrador, ListView): 
    model =  User


