import json
from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime

from prototype.models import Cage, Experiment, ExperimentGroup, Measurement, Mouse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/accounts/login/')
def dashboard(request):
    context = {
        'experiments': Experiment.objects.filter(owner=request.user)
    } 
    return render(request, "dashboard.html", context)

def home(request):
    if request.user.is_authenticated:
        return redirect('/prototype/dashboard')
    return render(request, "home.html")

def experiment_home(request, experiment_id):
    context = {
        'experiment': Experiment.objects.get(id=experiment_id)
        }
    return render(request, "experiment.html", context)

def cage_measurement(request, cage_id):
    if request.method == 'POST':
        date_string = request.POST.get('measure_date')
        mice = Cage.objects.get(id=cage_id).mice()
        for mouse in mice:
            mouse_measure = {}
            for item in request.POST:
                if f"mouse_{mouse.id}" in item:
                    mouse_measure[item]=request.POST.get(item)
            print(mouse_measure)

    context = {
        'cage': Cage.objects.get(id=cage_id),
        'date_string': datetime.now().strftime("%Y-%m-%d"),
        }
    return render(request, "cage.html", context)

def bulk_add(request, experiment_id):
    if request.method == 'POST':
        bulk_data = {
            "n": int(request.POST.get('n')),
            "start_id": int(request.POST.get('start_id')),
            "mpc": int(request.POST.get('mpc')),
            "start_cage": int(request.POST.get('start_cage'))
        }
        print(bulk_data)
        pref_ear_tags = ['N', 'R', 'L', 'B', 'RR', 'LL', 'BB']
        experiment=Experiment.objects.get(id=experiment_id)
        exp_group = ExperimentGroup(experiment=experiment, name="bulk add default group", description="group created to newly created mice before treatment assignment occurs")
        exp_group.save()
        for c in range(bulk_data['start_cage'], bulk_data['start_cage'] + (-(-bulk_data['n'] // bulk_data['mpc']))):
            cage = Cage(experiment = experiment, cage_number=c, external_id="NA")
            cage.save()
            et=-1
            for i in range(bulk_data['start_id'] + (c-bulk_data['start_cage']) * bulk_data['mpc'], bulk_data['start_id'] + (c+1-bulk_data['start_cage']) * bulk_data['mpc']):
                if i >= bulk_data['start_id'] + bulk_data['n']:
                    pass
                else:
                    et = et+1
                    print((c, i, pref_ear_tags[et]))
                    mouse = Mouse(
                        experiment_group=exp_group,
                        cage=cage,
                        ear_tag=pref_ear_tags[et],
                        experiment_id=i)
                    mouse.save()

    context = {
        "experiment": Experiment.objects.get(id=experiment_id)
    }
    return render(request, "bulk_add.html", context)


def volume_match(request, experiment_id):
    if request.method == 'POST':
        print(request.POST)
    context = {
        "experiment": Experiment.objects.get(id=experiment_id)
    }
    return render(request, "volume_match.html", context)
