from django.shortcuts import render, redirect
from .models import Action, Pacient_Schedule
import pandas as pd
import numpy as np
from django.conf import settings

def home(request):
    return render(request, 'action/index.html')

def upload(request):
    if request.method == 'POST':
        if request.POST['title'] and request.FILES['file']:
            action = Action()
            action.title = request.POST['title']
            action.file = request.FILES['file']
            action.save()
            return redirect(schedule, action.id)

def list_schedule(request):
    files = Action.objects.all()
    return render(request, 'action/list_schedule.html', {'files':files})

def schedule(request, action_id):
    action = Action.objects.get(id=action_id)
    return render(request, 'action/schedule.html', {'action':action})

def get_result(request, action_id):
    action = Action.objects.get(id=action_id)

    pacients_url = action.file.path
    doctors_url = settings.MEDIA_ROOT+'\\staticfiles\\csv_02_doctors.csv'

    pacients = pd.read_excel(pacients_url)

    doctors = pd.read_csv(doctors_url)
    doctors = doctors.drop('Unnamed: 0', axis=1)

    schedule = []

    for i in range(1, 37):
        took_pacients = []
        for j in range(len(doctors)):
            if(doctors['meet'+str(i)][j]!='-'):
                print(doctors['full_name'][j]+': '+doctors['meet'+str(i)][j])
                spec_of_doc = doctors['specialty'][j]
                for k in range(len(pacients)):
                    if (pacients[spec_of_doc][k] == 1 and (k not in took_pacients)):
                        took_pacients.append(k)
                        print(took_pacients)
                        schedule.append(doctors['full_name'][j])
                        schedule.append(spec_of_doc)
                        schedule.append(pacients['full_name'][k])
                        schedule.append(pacients['name'][k])
                        schedule.append(doctors['meet'+str(i)][j])
                        doctors['meet'+str(i)][j] = 0
                        pacients[spec_of_doc][k] = -1
                        break

    final_schedule = np.array(schedule).reshape(-1, 5)
    final_schedule = pd.DataFrame(final_schedule, columns='doc spec pacient let time'.split())
    dictionary = final_schedule.values
    print(final_schedule)
    # print(doctors)
    print(pacients)
    # print(dictionary)
    # print(len(dictionary))
    print(final_schedule[final_schedule['pacient']=='Barbara Smith'])
    example = Pacient_Schedule.objects.filter(title=pacients['full_name'][0]+'_'+str(action.title))
    if(example):
        pass
    else:
        for i in range(len(pacients)):
            pacient_name = pacients['full_name'][i]
            schedule1 = Pacient_Schedule()
            schedule1.title = pacient_name+'_'+str(action.title)
            final_schedule[final_schedule['pacient'] == pacient_name].to_csv('media/results/'+str(pacient_name).split()[0].lower()+str(pacients['id'][i])+'.csv')
            schedule1.file = 'results/'+str(pacient_name).split()[0].lower()+str(pacients['id'][i])+'.csv'
            schedule1.pacients_file_id = action_id
            schedule1.save()
    results = Pacient_Schedule.objects.filter(pacients_file_id=action_id)
    return render(request, 'action/result.html', {'results':results})