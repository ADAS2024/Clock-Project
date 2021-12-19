from tkinter import *
from tkinter.ttk import *
from tkinter.constants import CENTER, END, S
import datetime as dt
import platform as pt
import beepy as b

app_window = Tk()
app_window.title("My Clock")
app_window.geometry('500x250')
app_window.resizable(0, 0)
text_font = ("Times", 70, 'bold')
background = "#000000"
foreground = "#FFFFFF"
border_width = 30
stopwatch_counter_num = 104399
stopwatch_running = False
timer_counter_num = 104400
timer_running = False
toggledtime = "AM/PM"


def digital_clock():
    date_time = dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S/%p")
    date, time1 = date_time.split()
    time2, time3 = time1.split('/')
    hour, minutes, seconds = time2.split(':')
    if toggledtime == "AM/PM":
        if int(hour) > 12 and int(hour) < 24:
            time = str(int(hour) - 12) + ':' + minutes + ':' + seconds + ' ' + time3
        elif int(hour) == 00:
            time = "12" + ':' + minutes + ':' + seconds + ' ' + time3
        else:
            time = time2 + ' ' + time3
    else:
        if int(hour) >= 10 and int(hour) < 24:
            time = str(int(hour)) + ':' + minutes + ':' + seconds
        else:
            time = "0" + str(int(hour)) + ':' + minutes + ':' + seconds
    clock_label.config(text=time)
    date_label.config(text=date)
    clock_label.after(1000, digital_clock)


def alarm():
    if toggledtime == "AM/PM":
        mainAMPM_time = dt.datetime.now().strftime("%H:%M %p")
        alarm_timeAMPMmain = get_alarm_time_entry.get()
        alarm_timeAMPM, alarm_period = alarm_timeAMPMmain.split()
        alarm_hourAMPM, alarm_minutesAMPM = alarm_timeAMPM.split(':')
        main_timeAMPM, main_period = mainAMPM_time.split()
        main_hourAMPM, main_minutesAMPM = main_timeAMPM.split(':')
    else:
        mainMilitary_time = dt.datetime.now().strftime("%H:%M")
        alarm_timeMilitarymain = get_alarm_time_entry.get()
        alarm_hourMilitary, alarm_minutesMilitary = alarm_timeMilitarymain.split(':')
        main_hourMilitary, main_minutesMilitary = mainMilitary_time.split(':')

    if toggledtime == "AM/PM":
        if int(main_hourAMPM) > 12 and int(main_hourAMPM) < 24:
            main_hour = str(int(main_hourAMPM) - 12)
        else:
            main_hour = main_hourAMPM

    if toggledtime == "AM/PM":
        if int(alarm_hourAMPM) == int(main_hour) and int(alarm_minutesAMPM) == int(
                main_minutesAMPM) and alarm_period == main_period:
            for i in range(4):
                alarm_status_label.config(text='Time Is Up')
                b.beep(sound='ping')
            get_alarm_time_entry.config(state='enabled')
            set_alarm_button.config(state='enabled')
            get_alarm_time_entry.delete(0, END)
            alarm_status_label.config(text='')

        else:
            alarm_status_label.config(text='Alarm Has Started')
            get_alarm_time_entry.config(state='disabled')
            set_alarm_button.config(state='disabled')
        alarm_status_label.after(1000, alarm)

    else:
        if int(alarm_hourMilitary) == int(main_hourMilitary) and int(alarm_minutesMilitary) == int(
                main_minutesMilitary):
            for i in range(4):
                alarm_status_label.config(text='Time Is Up')
                b.beep(sound='ping')
            get_alarm_time_entry.config(state='enabled')
            set_alarm_button.config(state='enabled')
            get_alarm_time_entry.delete(0, END)
            alarm_status_label.config(text='')

        else:
            alarm_status_label.config(text='Alarm Has Started')
            get_alarm_time_entry.config(state='disabled')
            set_alarm_button.config(state='disabled')
        alarm_status_label.after(1000, alarm)


def stopwatch_counter(label):
    def count():
        if stopwatch_running:
            global stopwatch_counter_num
            if stopwatch_counter_num == 104399:
                display = "Starting..."
            else:
                tt = dt.datetime.fromtimestamp(stopwatch_counter_num)
                string = tt.strftime("%H:%M:%S")
                display = string
            label.config(text=display)
            label.after(1000, count)
            stopwatch_counter_num += 1

    count()


def stopwatch(work):
    if work == 'start':
        global stopwatch_running
        stopwatch_running = True
        stopwatch_start.config(state='disabled')
        stopwatch_stop.config(state='enabled')
        stopwatch_reset.config(state='enabled')
        stopwatch_counter(stopwatch_label)
    elif work == 'stop':
        stopwatch_running = False
        stopwatch_start.config(state='enabled')
        stopwatch_stop.config(state='disabled')
        stopwatch_reset.config(state='enabled')
    elif work == 'reset':
        global stopwatch_counter_num
        stopwatch_running = False
        stopwatch_counter_num = 104399
        stopwatch_label.config(text='Stopwatch')
        stopwatch_start.config(state='enabled')
        stopwatch_stop.config(state='disabled')
        stopwatch_reset.config(state='disabled')


def timer_counter(label):
    def count():
        global timer_running
        display = "Timer"
        if timer_running:
            global timer_counter_num
            if timer_counter_num == 104400:
                for i in range(3):
                    b.beep(sound='ping')
                timer_running = False
                timer('reset')
            else:
                tt = dt.datetime.fromtimestamp(timer_counter_num)
                string = tt.strftime("%H:%M:%S")
                display = string
                timer_counter_num -= 1
            label.config(text=display)
            label.after(1000, count)

    count()


def timer(work):
    if work == 'start':
        global timer_running, timer_counter_num
        timer_running = True
        if timer_counter_num == 104400:
            timer_time_str = timer_get_entry.get()
            hours, minutes, seconds = timer_time_str.split(':')
            minutes = int(minutes) + (int(hours) * 60)
            seconds = int(seconds) + (minutes * 60)
            timer_counter_num = timer_counter_num + seconds
        timer_counter(timer_label)
        timer_start.config(state='disabled')
        timer_stop.config(state='enabled')
        timer_reset.config(state='enabled')
        timer_get_entry.delete(0, END)
    elif work == 'stop':
        timer_running = False
        timer_start.config(state='enabled')
        timer_stop.config(state='disabled')
        timer_reset.config(state='enabled')
    elif work == 'reset':
        timer_running = False
        timer_counter_num = 104400
        timer_start.config(state='enabled')
        timer_stop.config(state='disabled')
        timer_reset.config(state='disabled')
        timer_get_entry.config(state='enabled')
        timer_label.config(text='Timer')


def toggletimebutton():
    global toggledtime
    if toggledtime == "AM/PM":
        toggledtime = "Military"
    else:
        toggledtime = "AM/PM"


tabs_control = Notebook(app_window)
clock_tab = Frame(tabs_control)
alarm_tab = Frame(tabs_control)
stopwatch_tab = Frame(tabs_control)
timer_tab = Frame(tabs_control)
timetoggle_tab = Frame(tabs_control)

tabs_control.add(clock_tab, text="Clock")
tabs_control.add(alarm_tab, text="Alarm")
tabs_control.add(stopwatch_tab, text='Stopwatch')
tabs_control.add(timer_tab, text='Timer')
tabs_control.add(timetoggle_tab, text='Standard/Military Time')
tabs_control.pack(expand=1, fill="both")

clock_label = Label(clock_tab, font=text_font, foreground=background)
clock_label.pack(anchor=CENTER)
date_label = Label(clock_tab, font=text_font, foreground=background)
date_label.pack(anchor=S)

stopwatch_label = Label(stopwatch_tab, font='Times 40 bold', text='Stopwatch')
stopwatch_label.pack(anchor='center')
stopwatch_start = Button(stopwatch_tab, text='Start', command=lambda: stopwatch('start'))
stopwatch_start.pack(anchor='center')
stopwatch_stop = Button(stopwatch_tab, text='Stop', state='disabled', command=lambda: stopwatch('stop'))
stopwatch_stop.pack(anchor='center')
stopwatch_reset = Button(stopwatch_tab, text='Reset', state='disabled', command=lambda: stopwatch('reset'))
stopwatch_reset.pack(anchor='center')

get_alarm_time_entry = Entry(alarm_tab, font="Times 12 bold")
get_alarm_time_entry.pack(anchor=CENTER)
alarm_instructions_label = Label(alarm_tab, font="Times 10 bold", text="Enter Alarm Time. Eg -> 01:30 PM or 13:30")
alarm_instructions_label.pack(anchor=S)
set_alarm_button = Button(alarm_tab, text="Set Alarm", command=alarm)
set_alarm_button.pack(anchor=S)
alarm_status_label = Label(alarm_tab, font="Times 12 bold")
alarm_status_label.pack(anchor=S)

timer_get_entry = Entry(timer_tab, font='Times 15 bold')
timer_get_entry.pack(anchor='center')
timer_instructions_label = Label(timer_tab, font='Times 8 bold',
                                 text="Enter Timer Time. Eg -> 01:30:30, 01 -> Hour, 30 -> Minutes, 30 -> Seconds")
timer_instructions_label.pack(anchor='s')
timer_label = Label(timer_tab, font='Times 40 bold', text='Timer')
timer_label.pack(anchor='center')
timer_start = Button(timer_tab, text='Start', command=lambda: timer('start'))
timer_start.pack(anchor='center')
timer_stop = Button(timer_tab, text='Stop', state='disabled', command=lambda: timer('stop'))
timer_stop.pack(anchor='center')
timer_reset = Button(timer_tab, text='Reset', state='disabled', command=lambda: timer('reset'))
timer_reset.pack(anchor='center')

toggle_instructions_label = Label(timetoggle_tab, font="Times 12 bold",
                                  text="Press button to swap between AM/PM and Military Time")
toggle_instructions_label.pack(anchor=S)
set_toggle_button = Button(timetoggle_tab, text='Change Time', command=toggletimebutton)
set_toggle_button.pack(anchor=S)

digital_clock()
app_window.mainloop()
