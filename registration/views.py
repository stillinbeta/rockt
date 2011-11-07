from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.template.response import TemplateResponse
from django.shortcuts import redirect

from forms import WaitingListForm, RegistrationForm
from models import BetaKey


def waiting_list(request):
    if request.method == "POST":
        form = WaitingListForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                "I'll contact you as soon as space is available")
            return redirect('home')
    else:
        form = WaitingListForm()

    return TemplateResponse(request, 'waiting-list.html', {'form': form})


def register(request, key):
    try:
        beta_key = BetaKey.objects.get(key=key)
        valid = beta_key.keys_available()
    except BetaKey.DoesNotExist:
        valid = False
    if not valid:
        messages.error(request, "This link is not valid")
        return redirect(waiting_list)
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth = authenticate(username=user.username,
                                password=form.cleaned_data['password1'])
            login(request, auth)
            beta_key.register_user(user)
            messages.success(request, "Welcome to Rockt!")
            return redirect('map')
    else:
        form = RegistrationForm()
    dic = {'form': form, 'key': key}
    return TemplateResponse(request, 'registration.html', dic)
