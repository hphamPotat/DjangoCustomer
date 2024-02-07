from django.shortcuts import render
from datetime import date, timedelta
from django.db.models import Count
from .models import *


def index(request):
    customer = Customer.objects.all()
    context = {'customers': customer}
    return render(request, 'index.html', context)


def create_customer(request):
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        social_media = request.POST['social_media']

        customer = Customer.objects.create(name=name, email=email, phone=phone, address=address, social_media=social_media)
        customer.save()
        return render(request, 'add.html', context={'msg': 'Created customer successfully'})

    return render(request, 'add.html')


def summary(request):
    past = date.today() - timedelta(days=30)
    interactions = Interaction.objects.filter(interaction_date__gte=past)
    count = len(interactions)
    interactions = interactions.values('channel', 'direction').annotate(count=Count('channel'))
    context = {
        'interactions': interactions,
        'count': count
    }

    return render(request, 'summary.html', context)


def interact(request, cid):
    channels = Interaction.CHANNEL_CHOICES
    directions = Interaction.DIRECTION_CHOICES
    context = {'channels': channels, 'directions': directions}

    if request.method == 'POST':
        customer = Customer.objects.get(id=cid)
        channel = request.POST["channel"]
        direction = request.POST["direction"]
        summary = request.POST["summary"]
        interaction = Interaction.objects.create(customer=customer, channel=channel, direction=direction, summary=summary)
        interaction.save()

        context['msg'] = 'Interaction Success'
    
    return render(request, 'interact.html', context)
