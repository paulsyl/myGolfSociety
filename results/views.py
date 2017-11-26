from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError
from django.db.models import Avg, Max
from django.contrib.auth.models import User
from datetime import date
from crispy_forms.helper import FormHelper
from .models import Event, Result, Player
from .forms import EventForm, PlayerForm
from string import ascii_uppercase


def todays_date():
    todays_date = date.today()
    today = todays_date.strftime("%Y-%m-%d")
    return today

@login_required
def dashboard(request):
    events = Event.objects.order_by('-date_of_event')
    members = Player.objects.order_by('last_name')
    context = {
        "events" : events,
        "members" : members
    }
    return render(request, 'results/dashboard.html', context)

@login_required
def events(request):
    events = Event.objects.order_by('-date_of_event')
    context = {
        "events" : events
    }
    return render(request, 'results/events.html', context)

@login_required
def members(request):
    members = []
    # loop through the alphabet and create a dicitionairy of each member per letter
    # istartwith is case insensitive search
    for alpha in ascii_uppercase:
        member_list = Player.objects.filter(last_name__istartswith=alpha)
        output = ( alpha, ( member_list ))
        members.append(output)

    context = {
        "members" : members
    }

    return render(request, 'results/members.html', context)

@login_required
def create_event(request):

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            event = form.save(commit=False)
            event.venue = form.cleaned_data['venue']
            event.date_of_event = form.cleaned_data['date_of_event']
            event.save

            Event.objects.create(venue=event.venue,
                                 date_of_event=event.date_of_event)

            return redirect('results:events')
    else:
        form = EventForm()

    return render(request, 'results/create_event.html', {"form": form})

@login_required
def create_player(request):

    if request.method == 'POST':
        form = PlayerForm(request.POST)

        if form.is_valid():
            player = form.save(commit=False)
            player.first_name = form.cleaned_data['first_name']
            player.last_name = form.cleaned_data['last_name']
            player.date_joined = todays_date()
            player.starting_handicap = form.cleaned_data['starting_handicap']
            player.save

            # Check to see if the player already exists
            player_check = Player.objects.filter(first_name=player.first_name, last_name=player.last_name)

            if player_check:
                render(request, 'results/create_player.html', {
                                                            "form": form,
                                                            "error": "ERROR: This player has already been created!"
                                                            })
                #  Need to figure out why error message is not returning
            else:
                Player.objects.create(first_name=player.first_name,
                                      last_name=player.last_name,
                                      date_joined=player.date_joined,
                                      starting_handicap=player.starting_handicap)

                return redirect('results:members')
    else:
        form = PlayerForm()

    return render(request, 'results/create_player.html', {"form": form})

@login_required
def get_event(request,fk):
    event = get_object_or_404(Event,pk=fk)
    result = Result.objects.filter(event_id=fk).order_by('event_rank')
    events = Event.objects.order_by('-date_of_event')
    context = {
            "result": result,
            "event": event,
            "events" : events
             }

    return render(request, 'results/getevent.html', context)

@login_required
def get_player_history(request,pk):
    player = get_object_or_404(Player,id=pk)
    avg_score = Result.objects.filter(player_id=pk).aggregate(Avg('total_score'))
    rds_played = Result.objects.filter(player_id=pk).count()
    history = Result.objects.filter(player_id=pk).order_by('-event__date_of_event')
    handicap_history = Result.objects.filter(player_id=pk).order_by('event__date_of_event')

    #Data values for the Handicap chart
    data_values = []
    for a in handicap_history:
        key_val = (a.event.date_of_event, a.handicap)
        data_values.append(key_val)

    context = {
        "history": history,
        "avg_score" : avg_score,
        "rds_played" : rds_played,
        "player" : player,
        "chart" : data_values,
    }
    return render(request, 'results/getplayerhistory.html', context)

def chart(request):
    pk = 16
    player = get_object_or_404(Player,id=pk)
    handicap_history = Result.objects.filter(player_id=pk).order_by('event__date_of_event')

    data_values = []

    for a in handicap_history:
        key_val = (a.event.date_of_event, a.handicap)
        data_values.append(key_val)

    context = {'values': data_values}
    return render(request, 'results/chart.html', context)
