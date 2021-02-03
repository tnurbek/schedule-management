from django.shortcuts import render, redirect
from django.conf import settings
from datetime import date, timedelta, datetime, time
import pandas as pd
from .models import Service, Device, DeviceSchedule, PointedSchedule
from pacient.models import Pacient
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg, Sum, Max, Count

def devices_home(request):
    devices = Device.objects.all()
    schedules = DeviceSchedule.objects.all()
    indices = []
    for i in schedules.all():
        indices.append(i.device_id)
    return render(request, 'device/devices.html', {'devices':devices, 'indices':indices})

def device(request, pk):
    device = Device.objects.get(id=pk)
    df = DeviceSchedule.objects.get(device_id=pk)
    # for i in range(160):
    #     print(schedule.__dict__['meet'+str(i+1)])
    timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
    timetable = pd.read_csv(timetable_url)
    final_time = []
    for i in range(len(timetable)):
        for j in range(1, 17):
            final_time.append(timetable['meet' + str(j)][i])
    time_list = []
    for i in range(160):
        time_list.append(i+1)
    date1 = date.today()
    weeknum = date1.isocalendar()[1]
    year = date1.year
    week_repr = str(year)+'-W'+str(weeknum)
    date1 = datetime.strptime(week_repr + '-1', '%G-W%V-%u').date()
    print(date1)
    days = [date1]
    for i in range(1, 7):
        duration = timedelta(days=i)
        days.append(date1 + duration)
    days_list = []
    for day in days:
        if day.weekday() != 6:
            days_list.append(str(day))
    output = ''
    for i in range(len(final_time)):
        output += '<tr>'
        output += '<td>' + final_time[i] + '</td>'
        for day in days:
            if day.weekday()!=6:
                schedule = PointedSchedule.objects.filter(device_id=pk, date__exact=str(day))
                app_time_list = [str(i.time) for i in schedule]
                if final_time[i] == df.__dict__['meet' + str(time_list[i])]:
                    output += '<td class="'
                    if final_time[i] in app_time_list:
                        output += 'bg-secondary'
                    else:
                        output += 'bg-success'
                    output += '"><input disabled type="checkbox" name="schedule" value="' + str(time_list[i]) + '" /></td>'
                elif df.__dict__['meet' + str(time_list[i])] == '-':
                        output += '<td class="bg-danger">-</td>'
        output += '</tr>'
        # print(output)
    patients = Pacient.objects.all()
    return render(request, 'device/device.html', {
        'device':device, 'output': output, 'days_list': days_list,
        'weeknum':weeknum, 'patients':patients
    })

def device2(request, pk):
    device = Device.objects.get(id=pk)
    df = DeviceSchedule.objects.get(device_id=pk)
    timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
    timetable = pd.read_csv(timetable_url)
    final_time = []
    for i in range(len(timetable)):
        for j in range(1,2):
            final_time.append(timetable['meet' + str(j)][i])
    time_list = []
    for i in range(len(timetable)):
        for j in range(1, 2):
            time_list.append(i*16+j)
    date1 = date.today()
    weeknum = date1.isocalendar()[1]
    year = date1.year
    week_repr = str(year)+'-W'+str(weeknum)
    date1 = datetime.strptime(week_repr + '-1', '%G-W%V-%u').date()
    days = [date1]
    for i in range(1, 7):
        duration = timedelta(days=i)
        days.append(date1 + duration)
    days_list = []
    for day in days:
        if day.weekday() != 6:
            days_list.append(str(day))
    output = ''
    for i in range(len(final_time)):
        time0 = final_time[i]
        time0 = datetime.strptime(time0, "%H:%M:%S")
        time1 = timedelta(hours=1)+time0
        time0 = time0.time()
        time1 = time1.time()
        output += '<tr>'
        output += '<td>' + str(time0)[:-3] + ' - ' + str(time1)[:-3] + '</td>'
        for day in days:
            fin_duration = 0
            if day.weekday()!=6:
                schedule = PointedSchedule.objects.filter(device_id=pk, date__exact=str(day), duration__gt=0)
                app_time_list = [str(i.time) for i in schedule]
                for t in schedule:
                    if t.time >= time0 and t.time < time1:
                        fin_duration += t.duration
                if final_time[i] == df.__dict__['meet' + str(time_list[i])]:
                    output += '<td class="'
                    # if final_time[i] in app_time_list:
                    if fin_duration == 60:
                        output += 'bg-secondary text-light'
                    elif fin_duration > 0:
                        output += 'bg-info'
                    else:
                        output += 'bg-success'
                    output += '">'+'<a href="#" class="text-light" onclick="my_func(\''+str(pk)+'\',\''+str(day)+'\',\''+str(time0)+'\')" data-toggle="modal" data-target="#exampleModal2">'+str(fin_duration)+' min</a>'+'</td>'
                elif df.__dict__['meet' + str(time_list[i])] == '-':
                        output += '<td class="bg-danger">-</td>'
        output += '</tr>'
        # print(output)
    stats = []
    total = -9*60
    for day in days:
        if day.weekday()!=6:
            durations = 0
            schedule = PointedSchedule.objects.filter(device_id=pk, date__exact=str(day))
            lst = [i.duration for i in schedule]
            for i in lst:
                durations += i
            stats.append(durations)
    patients = Pacient.objects.all()
    return render(request, 'device/device2.html', {
        'device':device, 'output': output, 'days_list': days_list,
        'weeknum':weeknum, 'patients':patients, 'stats':stats, 'total':total
    })

def set_schedule(request):
    if request.method == 'POST':
        device_id = request.POST['device_id']
        timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
        timetable = pd.read_csv(timetable_url)
        final_time = []
        for i in range(len(timetable)):
            for j in range(1, 17):
                final_time.append(timetable['meet' + str(j)][i])
        time_list = []
        for i in range(len(timetable)):
            for j in range(1, 17):
                time_list.append(i * 16 + j)
        schedule = DeviceSchedule()
        schedule.device_id = device_id
        for i in range(len(timetable)):
            for j in range(1, 17):
                if i+1 == j:
                    for k in range(1, 17):
                        index = i * 16 + k
                        thing = 'meet' + str(index)
                        schedule.__dict__[thing] = str(timetable['meet' + str(k)][i])
        schedule.save()
        return redirect('devices_home')

def reg_device_pacients(request, pk):
    pacient = Pacient.objects.get(id=pk)
    devices = Device.objects.all()
    history = PointedSchedule.objects.filter(pacient_id=pacient, duration__gt=0)
    return render(request, 'device/reg_pacient.html', {'pacient':pacient, 'devices':devices, 'history':history})

def get_services_of_device(request):
    if request.method == 'GET':
        device_id = request.GET['device_id']
        device = Device.objects.get(id=device_id)
        output = '<option></option>'
        for service in device.services.all():
            output += '<option value="'+str(service.id)+'">'+service.name+' ['+str(service.duration)+' min] '+'</option>'
        # print(output)
        data = {'output': output}
        return JsonResponse(data, safe=False)

def getdates_of_device(request):
    if request.method == 'GET':
        service_id = request.GET['service_id']
        device_name = request.GET['device_id']
        schedule = PointedSchedule.objects.filter(device__name__exact=device_name)
        service = Service.objects.get(id=service_id)
        duration = service.duration
        date1 = date.today()
        days = [date1]
        for i in range(1, 14):
            duration = timedelta(days=i)
            days.append(date1 + duration)
        days_list = []
        for day in days:
            if day.weekday() != 6:
                days_list.append(str(day))
        dates = '<option></option>'
        for day in days_list:
            dates += '<option value="' + day + '">' + day + '</option>'
        data = {'days_list': dates}
        return JsonResponse(data, safe=False)

def get_available_times_device(request):
    if request.method == 'GET':
        device_id = request.GET['device_id']
        service_id = request.GET['service_id']
        service = Service.objects.get(id=service_id)
        duration = service.duration
        lst5 = [1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 16]
        lst10 = [1, 3, 6, 9, 12, 15]
        lst12 = [1, 4, 7, 11, 14]
        lst15 = [1, 5, 9, 13]
        lst20 = [1, 6, 12]
        lst30 = [1, 9]
        dictionary = {'5': lst5, '10': lst10, '15': lst15, '12': lst12, '20': lst20, '30': lst30}
        lst = dictionary[str(duration)]
        timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
        timetable = pd.read_csv(timetable_url)
        final_time = []
        for i in range(len(timetable)):
            for j in lst:
                final_time.append(timetable['meet' + str(j)][i])
        day = request.GET['day']
        app_day = day  # we need it to check whether this time is chosen already or not
        schedule = DeviceSchedule.objects.filter(device_id=device_id)
        app_schedule = PointedSchedule.objects.filter(device_id=device_id, date__exact=app_day, is_done=False)
        app_time_list = [str(i.time) for i in app_schedule.all()] # all times in a given day as string
        print(app_time_list)
        if schedule:
            schedule = schedule[0]
            output = '<option></option>'
            time_list = []
            for i in range(1, 161):
                if schedule.__dict__['meet'+str(i)] in final_time:
                    time = schedule.__dict__['meet'+str(i)]
                    time1 = datetime.strptime(time, "%H:%M:%S")
                    time2 = time1 + timedelta(minutes=duration)
                    met = False
                    for eachtime in app_time_list:
                        time_to_check = datetime.strptime(eachtime, "%H:%M:%S")
                        if time_to_check > time1 and time_to_check < time2:
                            met = True
                    if time not in app_time_list and not met:
                        output += '<option value="'+time+'">'+time+'</option>'
                        time_list.append(schedule.__dict__['meet'+str(i)])
            data = {'times':time_list, 'output':output}
        else:
            data = {'times':'', 'output':''}
        return JsonResponse(data, safe=False)

def save_device_schedule(request, pk):
    if request.method == 'POST':
        pacient_id = pk
        device_id = request.POST['device_id']
        service_id = request.POST['service']
        service = Service.objects.get(id=service_id)
        date0 = request.POST['date']
        time0 = request.POST['time']
        time1 = datetime.strptime(time0, "%H:%M:%S")
        slack = timedelta(minutes=service.duration)
        time2 = time1 + slack
        time2 = time2.time()
        timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
        timetable = pd.read_csv(timetable_url)
        final_time = []
        for i in range(len(timetable)):
            for j in range(1, 17):
                final_time.append(timetable['meet' + str(j)][i])
        print(final_time)
        indices = []
        for i in range(len(final_time)):
            if datetime.strptime(final_time[i], "%H:%M:%S") >= datetime.strptime(time0, "%H:%M:%S") and datetime.strptime(final_time[i], "%H:%M:%S") < datetime.strptime(str(time2), "%H:%M:%S"):
                indices.append(i)
        schedule = PointedSchedule()
        schedule.pacient_id = pacient_id
        schedule.device_id = device_id
        schedule.service_id = service_id
        schedule.date = date0
        schedule.time = time0
        schedule.duration = service.duration
        schedule.save()
        for i in range(1, len(indices)):
            schedule_0 = PointedSchedule()
            schedule_0.date = date0
            schedule_0.time = final_time[indices[i]]
            schedule_0.pacient_id = pacient_id
            schedule_0.device_id = device_id
            schedule_0.service_id = service_id
            schedule_0.save()
        print(schedule)
        return redirect('reg_device_pacients', pacient_id)

def device_weekday(request, pk, weekday):
    device = Device.objects.get(id=pk)
    df = DeviceSchedule.objects.get(device_id=pk)
    timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
    timetable = pd.read_csv(timetable_url)
    final_time = []
    for i in range(len(timetable)):
        for j in range(1, 17):
            final_time.append(timetable['meet' + str(j)][i])
    time_list = []
    for i in range(160):
        time_list.append(i + 1)
    date1 = date.today()
    weeknum = weekday
    year = date1.year
    week_repr = str(year) + '-W' + str(weeknum)
    date1 = datetime.strptime(week_repr + '-1', '%G-W%V-%u').date()
    print(date1)
    days = [date1]
    for i in range(1, 7):
        duration = timedelta(days=i)
        days.append(date1 + duration)
    days_list = []
    for day in days:
        if day.weekday() != 6:
            days_list.append(str(day))
    output = ''
    for i in range(len(final_time)):
        output += '<tr>'
        output += '<td>' + final_time[i] + '</td>'
        for day in days:
            if day.weekday() != 6:
                schedule = PointedSchedule.objects.filter(device_id=pk, date__exact=str(day))
                app_time_list = [str(i.time) for i in schedule]
                if final_time[i] == df.__dict__['meet' + str(time_list[i])]:
                    output += '<td class="'
                    if final_time[i] in app_time_list:
                        output += 'bg-secondary'
                    else:
                        output += 'bg-success'
                    output += '"><input disabled type="checkbox" name="schedule" value="' + str(
                        time_list[i]) + '" /></td>'
                elif df.__dict__['meet' + str(time_list[i])] == '-':
                    output += '<td class="bg-danger">-</td>'
        output += '</tr>'
    patients = Pacient.objects.all()
    return render(request, 'device/device.html', {
        'device': device, 'output': output, 'days_list': days_list,
        'weeknum': weeknum, 'patients': patients
    })

def save_device_schedule2(request):
    if request.method == 'POST':
        pacient_id = request.POST['patient']
        device_id = request.POST['device_id']
        service_id = request.POST['service']
        service = Service.objects.get(id=service_id)
        date0 = request.POST['date']
        time0 = request.POST['time']
        time1 = datetime.strptime(time0, "%H:%M:%S")
        slack = timedelta(minutes=service.duration)
        time2 = time1 + slack
        time2 = time2.time()
        timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
        timetable = pd.read_csv(timetable_url)
        final_time = []
        for i in range(len(timetable)):
            for j in range(1, 17):
                final_time.append(timetable['meet' + str(j)][i])
        print(final_time)
        indices = []
        for i in range(len(final_time)):
            if datetime.strptime(final_time[i], "%H:%M:%S") >= datetime.strptime(time0, "%H:%M:%S") and datetime.strptime(final_time[i], "%H:%M:%S") < datetime.strptime(str(time2), "%H:%M:%S"):
                indices.append(i)
        schedule = PointedSchedule()
        schedule.pacient_id = pacient_id
        schedule.device_id = device_id
        schedule.service_id = service_id
        schedule.date = date0
        schedule.time = time0
        schedule.duration = service.duration
        schedule.save()
        for i in range(1, len(indices)):
            schedule_0 = PointedSchedule()
            schedule_0.date = date0
            schedule_0.time = final_time[indices[i]]
            schedule_0.pacient_id = pacient_id
            schedule_0.device_id = device_id
            schedule_0.service_id = service_id
            schedule_0.save()
        print(schedule)
        return redirect('device2', device_id)

def device_weekday2(request, pk, weekday):
    device = Device.objects.get(id=pk)
    df = DeviceSchedule.objects.get(device_id=pk)
    timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
    timetable = pd.read_csv(timetable_url)
    final_time = []
    for i in range(len(timetable)):
        for j in range(1, 2):
            final_time.append(timetable['meet' + str(j)][i])
    time_list = []
    for i in range(len(timetable)):
        for j in range(1, 2):
            time_list.append(i * 16 + j)
    date1 = date.today()
    weeknum = weekday
    year = date1.year
    week_repr = str(year) + '-W' + str(weeknum)
    date1 = datetime.strptime(week_repr + '-1', '%G-W%V-%u').date()
    print(date1)
    days = [date1]
    for i in range(1, 7):
        duration = timedelta(days=i)
        days.append(date1 + duration)
    days_list = []
    for day in days:
        if day.weekday() != 6:
            days_list.append(str(day))
    output = ''
    for i in range(len(final_time)):
        time0 = final_time[i]
        time0 = datetime.strptime(time0, "%H:%M:%S")
        time1 = timedelta(hours=1) + time0
        time0 = time0.time()
        time1 = time1.time()
        output += '<tr>'
        output += '<td>' + str(time0)[:-3] + ' - ' + str(time1)[:-3] + '</td>'
        for day in days:
            fin_duration = 0
            if day.weekday() != 6:
                schedule = PointedSchedule.objects.filter(device_id=pk, date__exact=str(day), duration__gt=0)
                app_time_list = [str(i.time) for i in schedule]
                for t in schedule:
                    if t.time >= time0 and t.time < time1:
                        fin_duration += t.duration
                if final_time[i] == df.__dict__['meet' + str(time_list[i])]:
                    output += '<td class="'
                    # if final_time[i] in app_time_list:
                    if fin_duration == 60:
                        output += 'bg-secondary text-light'
                    elif fin_duration > 0:
                        output += 'bg-info'
                    else:
                        output += 'bg-success'
                    output += '">' + '<a href="#" class="text-light" onclick="my_func(\'' + str(pk) + '\',\'' + str(
                        day) + '\',\'' + str(time0) + '\')" data-toggle="modal" data-target="#exampleModal2">' + str(
                        fin_duration) + ' min</a>' + '</td>'
                elif df.__dict__['meet' + str(time_list[i])] == '-':
                    output += '<td class="bg-danger">-</td>'
        output += '</tr>'
    stats = []
    total = -9 * 60
    for day in days:
        if day.weekday() != 6:
            durations = 0
            schedule = PointedSchedule.objects.filter(device_id=pk, date__exact=str(day))
            lst = [i.duration for i in schedule]
            for i in lst:
                durations += i
            stats.append(durations)
    patients = Pacient.objects.all()
    return render(request, 'device/device2.html', {
        'device': device, 'output': output, 'days_list': days_list,
        'weeknum': weeknum, 'patients': patients, 'stats':stats, 'total':total
    })

def get_specific_time_info(request):
    if request.method == 'GET':
        device_id = request.GET['device_id']
        date = request.GET['date']
        time = request.GET['start_time']
        time0 = datetime.strptime(time, "%H:%M:%S")
        time1 = timedelta(hours=1) + time0
        time0 = time0.time()
        time1 = time1.time()
        schedule = PointedSchedule.objects.filter(device_id=device_id, date__exact=date, duration__gt=0).order_by('time')
        output = ''
        for each in schedule:
            output += '<tr>'
            if(each.time >= time0 and each.time < time1):
                output += '<td>'+each.pacient.fullname+'</td>'
                output += '<td>'+str(each.time)[:-3]+'</td>'
                output += '<td>'+str(each.duration)+' min</td>'
                output += '<td><a href="/'+str(each.id)+'" class="btn-sm btn-primary">CHANGE</a></td>'
            output += '</tr>'
        response = {
            'output':output
        }
        return JsonResponse(response, safe=False)

def pointed_schedule(request, pk):
    schedule = PointedSchedule.objects.get(id=pk)
    pass

def patient_statistics(request):
    if request.method == 'GET':
        device_id = request.GET['device_id']
        date1 = date.today()
        weeknum = request.GET['week_number']
        year = date1.year
        week_repr = str(year) + '-W' + str(weeknum)
        date1 = datetime.strptime(week_repr + '-1', '%G-W%V-%u').date()
        days = [date1]
        for i in range(1, 7):
            duration = timedelta(days=i)
            days.append(date1 + duration)
        days_list = []
        for day in days:
            if day.weekday() != 6:
                days_list.append(str(day))
        week_schedule = PointedSchedule.objects.filter(device_id=device_id, date__in=days_list, duration__gt=0)
        summ = week_schedule.aggregate(Max('duration'), Count('duration'), Sum('duration'))
        patients = set()
        for each in week_schedule:
            patients.add(each.pacient_id)
        lst = []
        for patient in patients:
            number = 0
            duration_overall = 0
            for each in week_schedule:
                if patient == each.pacient_id:
                    number += 1
                    duration_overall += each.duration
            dct = dict()
            dct['fullname'] = Pacient.objects.get(id=patient).fullname
            dct['number'] = number
            dct['duration'] = duration_overall
            lst.append(dct)
        print(lst)
        output = ''
        for elem in lst:
            output += '<tr>'
            output += '<td>'+elem['fullname']+'</td>'
            if elem['number'] > 1:
                output += '<td>'+str(elem['number'])+' times</td>'
            else:
                output += '<td>' + str(elem['number']) + ' time</td>'
            output += '<td>'+str(elem['duration'])+' min</td>'
            output += '</tr>'
        print(output)
        response = {
            'output': output
        }
        return JsonResponse(response, safe=False)