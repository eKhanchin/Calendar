#!/usr/intel/bin/python -w


'''Created by: Eugeny Khanchin - 07 Jun 2020

This module contains a calendar widget.
'''


import datetime

from tkinter import *
from tkinter import ttk


class CalendarWidget:
    '''
    The widget returns date and time in a dictionary. To get this dictionary 
    you have to use a get_date_time() function.

    Attributes
    ----------
    master : object
        tkinter root window object
    date_time : dict
        A dictionary where every date and time element is a key

    Public Functions
    ----------------
    get_date_time() 
        Returns a dictionary of date and time elements

    Example
    -------
    root = tkinter.Tk()
    calendar = CalendarWidget(root)
    root.mainloop()
    date_time = calendar.get_date_time()
    # the keys are: 'year', 'month', 'day', 'hours', 'minutes' and 'seconds'
    print(date_time['year'])
    print(date_time['minutes'])
    '''

    def __init__(self, master):
        '''
        Parameters
        ----------
        master : object
            tkinter root window object
        '''

        self.master = master
        master.title('Calendar')
        master.geometry('520x275+200+100')
        master.resizable(False, False)

        # App's private variables
        self._months = self._get_month_names()
        self._months_days = self._get_months_days_dict()
        self._clicked_button = None
        self._date = ''
        self._time = ''
        self.date_time = {}

        # Configures style for app's widgets
        self._configure_style()

        ttk.Label(master, text='Select date and time').place(x=10, y=10)
        ttk.Frame(master, height=2, borderwidth=1, relief='flat', \
            style='Hor.TFrame')\
            .place(x=0, y=37, width=523)
        ttk.Frame(master, width=1, borderwidth=1, relief='flat', \
            style='Ver.TFrame')\
            .place(x=317, y=50, height=221)

        selected_date_label = ttk.Label(master, text='')
        selected_date_label.place(x=359, y=149)
        self._selected_date_label = selected_date_label

        # Date fields
        self._create_date_fields()

        # Time fields
        self._create_time_fields()

        ttk.Button(master, text='Select', command=self._select_date_time, \
            style='Select.TButton')\
            .place(x=360, y=226, width=120, height=40)

    def _get_month_names(self):
        '''Returns list of month names'''

        return ('January', 'February', 'March', 'April', 'May', 'June', \
            'July', 'August', 'September', 'October', 'November', 'December')
    
    def _get_months_days_dict(self):
        '''
        Returns a dictionary where keys are months and values are their 
        number of days
        '''

        months_days = {}
        months_days['January'] = 31
        months_days['February'] = 28
        months_days['March'] = 31
        months_days['April'] = 30
        months_days['May'] = 31
        months_days['June'] = 30
        months_days['July'] = 31
        months_days['August'] = 31
        months_days['September'] = 30
        months_days['October'] = 31
        months_days['November'] = 30
        months_days['December'] = 31

        return months_days

    def _configure_style(self):
        '''Contains all style configurations'''

        style = ttk.Style()

        # Root window's background color
        style.configure('TLabel', background='#e0dfde') 
        style.configure('TButton', background='#e0dfde')

        # Custom style
        # style.configure('TLabel', font=('default', 14))

        style.configure('Hor.TFrame', background='#6a9eba')
        style.configure('Ver.TFrame', background='#000000')

        style.configure('TCombobox', selectbackground=[('normal', 'white')])
        style.configure('TCombobox', selectforeground=[('normal', 'black')])

        style.configure('Day.TButton', background='#e0dfde', relief='flat')
        style.configure('Day.Clicked.TButton', background='#8cd0f5', \
            relief='flat')
        style.configure('Select.TButton', background='#6a9eba', \
            foreground='#ffffff', font=('', 12, 'bold'))

    def _create_date_fields(self):
        '''Creates all relevant to date fields'''

        # Month selection fields
        ttk.Label(self.master, text='Month:').place(x=10, y=50)
        self._month = StringVar()
        month_combobox = ttk.Combobox(self.master, width=9, \
            textvariable=self._month)
        month_combobox.place(x=58, y=50)
        month_combobox.bind('<<ComboboxSelected>>', self._enable_month_days)
        self._month_combobox = month_combobox
        self._load_months()

        # Year selection fields
        ttk.Label(self.master, text='Year:').place(x=183, y=50)
        self._year = StringVar()
        year_combobox = ttk.Combobox(self.master, width=9, \
            textvariable=self._year)
        year_combobox.place(x=222, y=50)
        year_combobox.bind('<<ComboboxSelected>>', self._enable_month_days)
        self._year_combobox = year_combobox 
        self._load_years()

        # Days of the month buttons
        days_buttons = []
        days = 31
        x = 35
        y = 87
        for i in range(1, days+1):
            # Creates a button with disabled state
            button = ttk.Button(self.master, text=str(i), style='Day.TButton')
            button.configure(command=lambda btn=button: \
                self._day_button_callback(btn))
            button.place(x=x, y=y, width=35, height=35)
            button.state(['disabled'])
            days_buttons.append(button)

            # Updates the x,y location
            x += 35
            if i % 7 == 0:
                x = 35
                y += 35
        self._days_buttons = days_buttons

    def _create_time_fields(self):
        '''Creates all relevant to time fields'''

        # Hour selection fields
        ttk.Label(self.master, text='Hours').place(x=331, y=50)
        hour_combobox = ttk.Combobox(self.master, width=3, values=[*range(0,24)])
        hour_combobox.place(x=333, y=70)
        hour_combobox.bind('<<ComboboxSelected>>', self._load_time)
        self._hour_combobox = hour_combobox

        # Minutes selection fields
        ttk.Label(self.master, text='Minutes').place(x=388, y=50)
        minutes_combobox = ttk.Combobox(self.master, width=3, \
            values=[*range(0,60)])
        minutes_combobox.place(x=396, y=70)
        minutes_combobox.bind('<<ComboboxSelected>>', self._load_time)
        self._minutes_combobox = minutes_combobox

        # Seconds selection fields
        ttk.Label(self.master, text='Seconds').place(x=456, y=50)
        seconds_combobox = ttk.Combobox(self.master, width=3, \
            values=[*range(0,60)])
        seconds_combobox.place(x=467, y=70)    
        seconds_combobox.bind('<<ComboboxSelected>>', self._load_time)
        self._seconds_combobox = seconds_combobox

    def _load_months(self):
        '''Loads months names into combobox'''
                 
        self._month_combobox.configure(values=self._months)
    
    def _load_years(self):
        '''Loads years into combobox beggining from 1990'''

        now = datetime.datetime.now()

        years = [*range(1990, now.year+1)]
        years.reverse()
        
        self._year_combobox.configure(values=years)

    def _enable_month_days(self, event=None):
        '''Enables relevant days of a selected month'''

        month = self._month_combobox.get()
        year = self._year_combobox.get()

        if month and year:
            # Fields are not empty
            days = self._months_days[month]

            year = int(year)
            if month == 'February' and year % 4 == 0:
                # Leap year - 29 days
                days += 1
            
            i = 0
            while i <= days-1:
                # Enables days of a month
                self._days_buttons[i].state(['!disabled'])
                self._days_buttons[i].configure(style='Day.TButton')
                i += 1
            
            while i < 31:
                # Disables days that exceed the number of days in a month
                self._days_buttons[i].state(['disabled'])
                self._days_buttons[i].configure(style='Day.TButton')
                i += 1
            
            self._selected_date_label.configure(text='')
        
    def _day_button_callback(self, button):
        '''A callback of a days of the month button'''

        if self._clicked_button:
            self._clicked_button.configure(style='Day.TButton')
        
        button.configure(style='Day.Clicked.TButton')
        self._clicked_button = button

        # Updates selected_date_label text
        month = self._month_combobox.get()
        month = str(self._months.index(month)+1)
        day = button.cget('text')
        year = self._year_combobox.get()

        date = month + '/' + day + '/' + year
        self._date = date
        
        self._update_date_time_label()
    
    def _load_time(self, event=None):
        '''Time selection fields\' callback'''

        hour = self._hour_combobox.get()
        minutes = self._minutes_combobox.get()
        seconds = self._seconds_combobox.get()

        if hour and minutes and seconds:
            # No empty fields
            if int(hour) < 10:
                hour = '0' + hour
            
            if int(minutes) < 10:
                minutes = '0' + minutes
            
            if int(seconds) < 10:
                seconds = '0' + seconds

            time = hour + ':' + minutes + ':' + seconds
            self._time = time

            self._update_date_time_label()
    
    def _update_date_time_label(self):
        '''Updates date and time label'''

        if self._date and self._time:
            self._selected_date_label.configure(\
                text=self._date + '   ' + self._time)
    
    def _select_date_time(self):
        '''Creates and saves a dictionary of date and time.
        
        After a dictionary is created the window is closed.
        '''

        month = self._month_combobox.get()
        year = self._year_combobox.get()

        day = ''
        if self._clicked_button:
            day = self._clicked_button.cget('text')

        hour = self._hour_combobox.get()
        minutes = self._minutes_combobox.get()
        seconds = self._seconds_combobox.get()

        if month and year and day and hour and minutes and seconds:

            date_time = {}
        
            month = str(self._months.index(month)+1)
            if int(month) < 10:
                month = '0' + month

            if int(day) < 10:
                day = '0' + day

            date_time['month'] = month
            date_time['year'] = year
            date_time['day'] = day

            if int(hour) < 10:
                hour = '0' + hour
            
            if int(minutes) < 10:
                minutes = '0' + minutes
            
            if int(seconds) < 10:
                seconds = '0' + seconds

            date_time['hour'] = hour
            date_time['minutes'] = minutes
            date_time['seconds'] = seconds

            self.date_time = date_time

            self.master.destroy()
    
    def get_date_time(self):
        '''Returns a dictionary of date and time elements'''

        return self.date_time