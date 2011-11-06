import json

from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import messages

from game.models import Car, Event
from game.rules import get_rule
from game.forms import ProfileForm


@login_required
def fleet_map(request):
    dic = {'selected': 'map'}
    car_set = request.user.get_profile().car_set.all()
    dic['cars'] = json.dumps([
                   {'number': car.number,
                   'location': car.location,
                   'route': car.route,
                   'url': reverse('car', args=(car.number,))}
                   for car in car_set])

    return TemplateResponse(request, 'map.html', dic)


@login_required
def fleet(request):
    dic = {'selected': 'fleet'}
    car_set = request.user.get_profile().car_set.all()
    dic['cars'] = [{'number': car.number,
                    'revenue': car.owner_fares.revenue} for car in car_set]
    return TemplateResponse(request, 'fleet.html', dic)


@login_required
def car(request, number):
    try:
        car = Car.objects.get(number=number)
    except Car.DoesNotExist:
        raise Http404
    if not car.owner == request.user.get_profile():
        messages.error(request, 'Not allowed')
        return redirect('map')
    events = Event.objects.get_car_timeline(car)
    dic = {'car': car, 'timeline': events}
    return TemplateResponse(request, 'car.html', dic)


@login_required
def sell(request, number):
    try:
        car = Car.objects.get(number=number)
    except Car.DoesNotExist:
        raise Http404
    if not car.owner == request.user.get_profile():
        messages.error(request, 'Not allowed')
        return redirect('map')
    if request.method == 'POST':
        try:
            confirm = request.POST['confirm']
            car.buy_back(request.user)
        except KeyError:
            #Continue to rendering the page as usual
            pass
        except Car.NotAllowedException:
            messages.error(request, 'Not allowed')
            return redirect('map')
        else:
            messages.success(request, 'Sold!')
            return redirect(fleet)
    dic = {'number': car.number,
           'price': get_rule('RULE_GET_STREETCAR_PRICE', request.user, car)}
    return TemplateResponse(request, 'sell.html', dic)


@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.user, request.POST)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile Updated")
            redirect(profile)
    else:
        profile_form = ProfileForm(request.user)
    dic = {'form': profile_form}
    return TemplateResponse(request, 'profile.html', dic)
