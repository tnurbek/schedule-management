from django.shortcuts import render, redirect
from .models import Pacient, Schedule
from resource.models import Specialty, Doctor, ScheduleDoctor
from datetime import date, time, timedelta, datetime
from django.http import JsonResponse

def pacients_home(request):
    pacients = Pacient.objects.all()
    specialties = Specialty.objects.all()
    schedule = Schedule.objects.filter(is_done=False, date__gte=date.today())
    return render(request, 'pacient/pacients.html', {'pacients': pacients, 'specialties': specialties, 'schedule':schedule})

def specific_pacient(request, pk):
    pacient = Pacient.objects.get(id=pk)
    day = date.today()
    schedule = Schedule.objects.filter(pacient_id=pk, is_done=False, date__gte=day)
    history = Schedule.objects.filter(pacient_id=pk)
    return render(request, 'pacient/pacient.html', {'pacient':pacient, 'schedule':schedule, 'history':history})

def create_pacient(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        specialties = request.POST.getlist('specialty')
        specs = [int(i) for i in specialties]
        pacient = Pacient()
        pacient.fullname = fullname
        pacient.save()
        for i in specs:
            pacient.specialty.add(i)
        pacient.save()
        return redirect('pacients_home')

def getdocs_by_spec(request):
    if request.method == 'GET':
        spec_id = request.GET['specialty_id']
        doctors = Doctor.objects.filter(specialty_id=spec_id)
        output = '<option></option>'
        for doctor in doctors:
            output += '<option value="'+str(doctor.id)+'">'+doctor.fullname+'</option>'
        # data = list(doctors.values())
        data = {'output':output}
        return JsonResponse(data, safe=False)

def getdates_by_doc(request):
    if request.method == 'GET':
        doctor_id = request.GET['doctor_id']
        date1 = date.today()
        days = [date1]
        for i in range(1, 14):
            duration = timedelta(days=i)
            days.append(date1 + duration)
        schedule = ScheduleDoctor.objects.filter(doctor_id=doctor_id)
        weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weeks_list = [each.weekday for each in schedule]
        days_list = []
        for day in days:
            if weeks[day.weekday()] in weeks_list:
                days_list.append(str(day))
        dates = '<option></option>'
        for day in days_list:
            dates += '<option value="'+day+'">'+day+'</option>'
        data = {'days_list':dates}
        return JsonResponse(data, safe=False)

def get_available_times(request):
    if request.method == 'GET':
        doctor_id = request.GET['doctor_id']
        day = request.GET['day']
        app_day = day  # we need it to check whether this time is chosen already or not
        day = datetime.strptime(day, "%Y-%m-%d").date()
        weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday = day.weekday()
        week = weeks[int(weekday)]
        schedule = ScheduleDoctor.objects.filter(doctor_id=doctor_id, weekday=week)
        app_schedule = Schedule.objects.filter(doctor_id=doctor_id, date__exact=app_day, is_done=False)
        app_time_list = [str(i.time) for i in app_schedule.all()] # all times in a given day as string
        print(app_time_list)
        if schedule:
            schedule = schedule[0]
            output = '<option></option>'
            time_list = []
            for i in range(1, 161):
                if schedule.__dict__['meet'+str(i)] != '-':
                    time = schedule.__dict__['meet'+str(i)]
                    if time not in app_time_list:
                        output += '<option value="'+time+'">'+time+'</option>'
                        time_list.append(schedule.__dict__['meet'+str(i)])
            data = {'times':time_list, 'output':output}
        else:
            data = {'times':'', 'output':''}
        return JsonResponse(data, safe=False)

def save_schedule(request, pk):
    if request.method == 'POST':
        pacient_id = pk
        doctor_id = request.POST['doctor']
        date0 = request.POST['date']
        time0 = request.POST['time']
        schedule = Schedule()
        schedule.pacient_id = pacient_id
        schedule.doctor_id = doctor_id
        schedule.date = date0
        schedule.time = time0
        schedule.save()
        print(schedule)
        return redirect('specific_pacient', pacient_id)

def control(request):
    if 'search' in request.GET:
        schedule = Schedule.objects.filter(doctor__fullname__contains=request.GET['search'], is_done=False).order_by('date', 'time')
    else:
        schedule = Schedule.objects.filter(is_done=False).order_by('date', 'time')
    return render(request, 'pacient/controller_page.html', {'schedule':schedule})

def meeting_done(request):
    if request.method == 'POST':
        schedule_id = request.POST['check']
        schedule = Schedule.objects.get(id=schedule_id)
        schedule.is_done = True
        schedule.save()
        return redirect('controller')
        # return JsonResponse(response)