from django.template import RequestContext
from django.shortcuts import render_to_response, render, HttpResponseRedirect, HttpResponse
#from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import *
from accounts.models import UserProfile
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@login_required() # only logged in users should access this
def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, UserProfile, fields=('website', 'bio', 'phone', 'city', 'country', 'organization'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect('/accounts/profile/')

        return render(request, "account_update.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


@csrf_exempt
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username = form.cleaned_data['username'],
                                            password = form.cleaned_data['password1'],
                                            email = form.cleaned_data['email'])
            return HttpResponse(status=200)
    else:
        form = RegistrationForm()
    return render(request,'registration/register.html',{'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=200)

def main_page(request):
    return render(request, 'main_page.html')

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
