from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
import pandas as pd
from .models import Doctor, ScheduleDoctor
from pacient.models import Schedule
from datetime import date, timedelta


def coordinator_page(request):
    doctors_list = Doctor.objects.all()
    return render(request, 'resource/coordination.html', {'doctors': doctors_list})


def save_schedule(request):
    if request.method == 'POST':
        doctor_id = request.POST['doctor']
        weekday = request.POST['weekday']
        duration = request.POST['duration']
        doctor = Doctor.objects.get(id=doctor_id)
        if doctor.duration == 0:
            doctor.duration = duration
            doctor.save()
        schedule_exists = ScheduleDoctor.objects.filter(weekday=weekday, doctor_id=doctor_id)
        work1_start_time = int(request.POST['work1_start']) if request.POST['work1_start'] else 0
        work1_end_time = int(request.POST['work1_end']) if request.POST['work1_end'] else 0
        work2_start_time = int(request.POST['work2_start']) if request.POST['work2_start'] else 0
        work2_end_time = int(request.POST['work2_end']) if request.POST['work2_end'] else 0
        timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
        df = pd.read_csv(timetable_url)
        lst5 = [1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 16]
        lst10 = [1, 3, 6, 9, 12, 15]
        lst12 = [1, 4, 7, 11, 14]
        lst15 = [1, 5, 9, 13]
        lst20 = [1, 6, 12]
        lst30 = [1, 9]
        dictionary = {'5': lst5, '10': lst10, '15': lst15, '12': lst12, '20': lst20, '30': lst30}
        if doctor_id and weekday and duration and (
                (work1_start_time and work1_end_time) or (work2_start_time and work2_end_time)):
            if not schedule_exists:
                lst = dictionary[str(duration)]
                schedule = ScheduleDoctor()
                schedule.doctor_id = doctor_id
                schedule.weekday = weekday
                for i in range(len(df)):
                    for j in range(work1_start_time, work1_end_time):
                        if i + 1 == j:
                            for k in lst:
                                index = i * 16 + k
                                thing = 'meet' + str(index)
                                schedule.__dict__[thing] = str(df['meet' + str(k)][i])
                    for j in range(work2_start_time, work2_end_time):
                        if i + 1 == j:
                            for k in lst:
                                index = i * 16 + k
                                schedule.__dict__['meet' + str(index)] = str(df['meet' + str(k)][i])
                schedule.save()
                return redirect('coordinator_page')
            else:
                print('it exists already!')
        else:
            print('no')


def doctors_schedule(request):
    doctors_list = Doctor.objects.all()
    weekdays = {'monday': 'Понедельник', 'tuesday': 'Вторник', 'wednesday': 'Среда', 'thursday': 'Четверг',
                'friday': 'Пятница', 'saturday': 'Суббота'}
    return render(request, 'resource/schedule.html', {'doctors': doctors_list, 'weekdays': weekdays})


def doctors_search(request):
    if request.method == 'GET':
        search_text = request.GET['search']
        doctors_list = Doctor.objects.filter(fullname__contains=search_text)
        output = ''
        for doctor in doctors_list:
            output += '<tr>'
            output += '<td>' + str(doctor.id) + '</td>'
            output += '<td>' + doctor.fullname + '</td>'
            output += '<td>' + doctor.specialty.specialty_name + '</td>'
            output += '<td><a href="/resources/doctors_schedule/' + str(
                doctor.id) + '" class="btn-sm btn-dark">SEE</a></td>'
            output += '</tr>'
        response = {'output': output}
        return JsonResponse(response)


def specific_schedule(request, pk):
    doctor_id = pk
    df = ScheduleDoctor.objects.select_related('doctor').filter(doctor_id=doctor_id)
    doctor = Doctor.objects.get(id=doctor_id)
    lst5 = [1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 16]
    lst10 = [1, 3, 6, 9, 12, 15]
    lst12 = [1, 4, 7, 11, 14]
    lst15 = [1, 5, 9, 13]
    lst20 = [1, 6, 12]
    lst30 = [1, 9]
    dictionary = {'5': lst5, '10': lst10, '15': lst15, '12': lst12, '20': lst20, '30': lst30}
    lst = dictionary[str(doctor.duration)]
    timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
    timetable = pd.read_csv(timetable_url)
    final_time = []
    for i in range(len(timetable)):
        for j in lst:
            final_time.append(timetable['meet' + str(j)][i])
    time_list = []
    for i in range(len(timetable)):
        for j in lst:
            time_list.append(i * 16 + j)
    date1 = date.today()
    days = [date1]
    for i in range(1, 14):
        duration = timedelta(days=i)
        days.append(date1 + duration)
    weeks = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weeks_list = []
    days_list = []
    for day in days:
        weeks_list.append(weeks[day.weekday()])
        days_list.append(str(day))
    work_week_list = [x.weekday for x in df]
    output = ''
    for i in range(len(final_time)):
        output += '<tr>'
        output += '<td>' + final_time[i] + '</td>'
        for day in days:
            each = weeks[day.weekday()]
            schedule = Schedule.objects.filter(doctor_id=pk, date__exact=str(day))
            app_time_list = [str(i.time) for i in schedule]
            if each in [x for x in work_week_list]:
                for elem in df:
                    if final_time[i] == elem.__dict__['meet' + str(time_list[i])]:
                        if elem.weekday == each:
                            output += '<td class="'
                            if final_time[i] in app_time_list:
                                output += 'bg-secondary'
                            else:
                                output += 'bg-success'
                            output += '"><input disabled type="checkbox" name="schedule" value="' + each + ' ' + str(time_list[i]) + '" /></td>'

                    elif elem.__dict__['meet' + str(time_list[i])] == '-':
                        if elem.weekday == each:
                            output += '<td class="bg-danger">-</td>'
            else:
                output += '<td >' + each[:2] + '</td>'
        output += '</tr>'
    response = {'text': output}
    return render(request, 'resource/specific_schedule.html',
                  {'output': output, 'doctor': doctor, 'weeks_list': weeks_list, 'days_list': days_list})


def doctor_info(request):
    if request.method == 'GET':
        doctor_id = request.GET['doctor_id']
        df = ScheduleDoctor.objects.select_related('doctor').filter(doctor_id=doctor_id)
        # print(df.query)
        # df = ScheduleDoctor.objects.raw('SELECT id, doctor_id, weekday FROM resource_scheduledoctor WHERE doctor_id = %s', [doctor_id])
        doctor = Doctor.objects.get(id=doctor_id)
        lst5 = [1, 2, 3, 5, 6, 8, 9, 10, 12, 13, 15, 16]
        lst10 = [1, 3, 6, 9, 12, 15]
        lst12 = [1, 4, 7, 11, 14]
        lst15 = [1, 5, 9, 13]
        lst20 = [1, 6, 12]
        lst30 = [1, 9]
        dictionary = {'5': lst5, '10': lst10, '15': lst15, '12': lst12, '20': lst20, '30': lst30}
        lst = dictionary[str(doctor.duration)]
        timetable_url = settings.MEDIA_ROOT + '\\staticfiles\\time_schedule.csv'
        timetable = pd.read_csv(timetable_url)
        final_time = []
        for i in range(len(timetable)):
            for j in lst:
                final_time.append(timetable['meet' + str(j)][i])
        time_list = []
        for i in range(len(timetable)):
            for j in lst:
                time_list.append(i * 16 + j)
        week_list = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        work_week_list = [x.weekday for x in df]
        output = ''
        for i in range(len(final_time)):
            output += '<tr>'
            output += '<td>' + final_time[i] + '</td>'
            for each in week_list:
                if each in [x for x in work_week_list]:
                    for elem in df:
                        if final_time[i] == elem.__dict__['meet' + str(time_list[i])]:
                            if elem.weekday == each:
                                output += '<td class="bg-success"><input type="checkbox" name="schedule" value="' + each + ' ' + str(
                                    time_list[i]) + '"></td>'
                        elif elem.__dict__['meet' + str(time_list[i])] == '-':
                            if elem.weekday == each:
                                output += '<td class="bg-danger">-</td>'
                else:
                    output += '<td class="bg-info"></td>'
            output += '</tr>'
        response = {'text': output}
    return JsonResponse(response)


def get_duration(request):
    if request.method == 'GET':
        doctor_id = request.GET['doctor_id']
        doctor = Doctor.objects.get(id=doctor_id)
    response = {'duration': doctor.duration}
    return JsonResponse(response)


def get_times(request):
    response = ''
    if request.method == 'GET':
        doctor_id = request.GET['doctor_id']
        weekday = request.GET['weekday']
        schedule = ScheduleDoctor.objects.filter(doctor_id=doctor_id, weekday=weekday)
        # duration = Doctor.objects.get(doctor_id).duration
        work1_start_time, work1_end_time, work2_start_time, work2_end_time = '', '', '', ''
        index = 0
        index_2 = 0
        for i in range(1, 161):
            if schedule[0].__dict__['meet' + str(i)] != '-' and index == 0 and i < 80:
                index = i
                work1_start_time = schedule[0].__dict__['meet' + str(i)]
            if schedule[0].__dict__['meet' + str(i)] != '-' and index != 0 and i < 80:
                work1_end_time = schedule[0].__dict__['meet' + str(i)]
            if schedule[0].__dict__['meet' + str(i)] != '-' and index_2 == 0 and i > 80:
                index_2 = i
                work2_start_time = schedule[0].__dict__['meet' + str(i)]
            if schedule[0].__dict__['meet' + str(i)] != '-' and index_2 != 0:
                work2_end_time = schedule[0].__dict__['meet' + str(i)]
        work1_start_time = work1_start_time[:5] if work1_start_time else ''
        work1_end_time = str(int(work1_end_time[:2]) + 1) + ':00' if work1_end_time else ''
        work2_start_time = work2_start_time[:5] if work2_start_time else ''
        work2_end_time = str(int(work2_end_time[:2]) + 1) + ':00' if work2_end_time else ''
        lst1 = ['08:00', '09:00', '10:00', '11:00', '12:00']
        lst2 = ['09:00', '10:00', '11:00', '12:00', '13:00']
        lst3 = ['14:00', '15:00', '16:00', '17:00']
        lst4 = ['15:00', '16:00', '17:00', '18:00']
        output1 = '<option value=""></option>'
        for i in range(len(lst1)):
            output1 += '<option selected value="' + str(i + 1) + '">' + lst1[i] + '</option>' if lst1[
                                                                                                     i] == work1_start_time else '<option value="' + str(
                i + 1) + '">' + lst1[i] + '</option>'
        output2 = '<option value=""></option>'
        for i in range(len(lst2)):
            output2 += '<option selected value="' + str(i + 2) + '">' + lst2[i] + '</option>' if lst2[
                                                                                                     i] == work1_end_time else '<option value="' + str(
                i + 2) + '">' + lst2[i] + '</option>'
        output3 = '<option value=""></option>'
        for i in range(len(lst3)):
            output3 += '<option selected value="' + str(i + 7) + '">' + lst3[i] + '</option>' if lst3[
                                                                                                     i] == work2_start_time else '<option value="' + str(
                i + 7) + '">' + lst3[i] + '</option>'
        output4 = '<option value=""></option>'
        for i in range(len(lst4)):
            output4 += '<option selected value="' + str(i + 8) + '">' + lst4[i] + '</option>' if lst4[
                                                                                                     i] == work2_end_time else '<option value="' + str(
                i + 8) + '">' + lst4[i] + '</option>'
        response = {
            'work1_start': output1,
            'work1_end': output2,
            'work2_start': output3,
            'work2_end': output4,
        }
    return JsonResponse(response)
