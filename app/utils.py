from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(date__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li> {event.title} </li>'

		if day != 0:
			return f"<td><span class='date'>{day}</td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(date__year=self.year, date__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		cal += f'</table>'
		return cal

class Eventcal(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Eventcal, self).__init__()

	# formats a day as a td
	# filter events by day
	def eventlist(self, day, events):
		events_per_day = events.filter(date__day=day)
		d = ''
		for event in events_per_day:
			d += f'<li>{event.date} {event.get_html_url} </li>'

		return f"<ul> {d} </ul></td>"

	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.eventlist(d, events)
		return f'{week}'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(date__year=self.year, date__month=self.month)

		event = f'<ol>'
		for week in self.monthdays2calendar(self.year, self.month):
			event += f'{self.formatweek(week, events)}\n'
		event += f'</ol>'
		return event