from calendar import HTMLCalendar
from .models import Event

class Calendar(HTMLCalendar):
	def __init__(self, year, month, today_date, today_month, today_year):
		self.year = year
		self.month = month
		self.today_date = today_date
		self.today_month = today_month
		self.today_year = today_year
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day,weekday, events): 
		events_per_day = events.filter(date__day=day)
		weekdays = "mon" if  weekday == 0 else "tue" if weekday == 1 else "wed" if weekday == 2 else "thu" if weekday == 3 else "fri" if weekday == 4 else "sat" if weekday == 5 else "sun"
		d = ''  
		bgColor=""
		for event in events_per_day: 
			if event.category == "Birthday": 
				d += f'<a style ="background-color : #ffc14e; margin:2px; display:inline-block;border-radius:50px;width:7px; height:7px;" >&nbsp;</a>'
			elif event.category == "Event":
				d += f'<a style ="background-color : #009eff;margin:2px; display:inline-block;border-radius:50px;width:7px;height:7px;">&nbsp;</a>'
			elif event.category == "Public Holiday":
				d += f'<a style ="background-color : #eb5353;margin:2px; display:inline-block;border-radius:50px;width:7px;height:7px;">&nbsp;</a>'
			else:
				d += f'<a style ="background-color : #fff; margin:2px; display:inline-block;border-radius:50px;width:7px;height:7px;">&nbsp; </a>'
		cells = ""  
		if day != 0:
			if self.year == self.today_year:
				if self.month == self.today_month:
					if  day == self.today_date:
						return f"<td class='activee {weekdays}'style  = 'background-color :{bgColor};><span class='date'>{day}<ul style=' width:100%; margin-left:0px;'>{d}</ul></td>"  
					return f"<td class='{weekdays}'  ><span class='date'>{day}<ul style='margin-left:0px; width:100%;'>{d}</ul></td>"
				return f"<td class='{weekdays}' ><span class='date'>{day}<ul style='margin-left:0px; width:100%;'>{d}</ul></td>"
			else:
				return f"<td class='{weekdays}'style  = 'background-color :{bgColor};><span class='date'>{day}<ul style='margin-left:0px; width:100%;'>{d}</ul></td>"
		return '<td class="%s %s"></td>' %(self.cssclass_noday, weekdays)

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d,weekday, events)
		return f'<tr class="days" > {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(date__year=self.year, date__month=self.month)

		cal = f'<table  cellpadding="0" cellspacing="0" style="border:none;width:100%; " class="calendar">\n'
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
			if(event.category == "Event"):
				d += f'<li><div class = "row">  <div class="col-md-1"><div class = "event"></div> </div>  <div class="col-md-7"><span class="date"> {event.date}</span><br><br><span class = "title">"><a style="color:#009eff;cursor:pointer;"  data-bs-toggle="modal" data-bs-target="#desModal  ">{event.title} </a>"><a  href={event.get_event_description}>{event.title} </a></span></div>  <div class="col-md-3">  <div class="row" style="margin-left:20%;"> {event.get_html_url}</div>    <div class="row" style="margin-left:20%;"> {event.deleteEvent}</div>  </div> </div></li><div class="modal fade     "style="margin-top:13%;"id="desModal" tabindex="-1" aria-labelledby="desModalLabel" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"><h5 class="modal-title" id="desModalLabel">Event Description</h5></div><div class="modal-body"> <p>{event.get_event_description}</p> </div> <div class="modal-footer"><button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button></div></div></div></div>'
			elif (event.category == "Birthday"): 
				d += f'<li><div class = "row">  <div class="col-md-1"><div class = "birthday"></div> </div>  <div class="col-md-7"><span class="date"> {event.date}</span><br><br><span class = "title"> <a style="color:#009eff; cursor:pointer;" data-bs-toggle="modal" data-bs-target="#desModal1  ">{event.title} </a></span></div>  <div class="col-md-3">  <div class="row" style="margin-left:20%;"> {event.get_html_url}</div>    <div class="row" style="margin-left:20%;"> {event.deleteEvent}</div>  </div> </div></li><div class="modal fade   "style="margin-top:13%;"id="desModal1" tabindex="-1" aria-labelledby="desModal1Label" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"><h5 class="modal-title" id="desModalLabel">Event Description</h5></div><div class="modal-body"> <p>{event.get_event_description}</p> </div> <div class="modal-footer"><button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button></div></div></div></div>'
			else:
				d += f'<li><div class = "row">  <div class="col-md-1"><div class = "publicHoliday"></div> </div>  <div class="col-md-7"><span class="date"> {event.date}</span><br><br><span class = "title"><a style="color:#009eff;cursor:pointer;" data-bs-toggle="modal" data-bs-target="#desModal2  ">{event.title} </a></span></div>  <div class="col-md-3">  <div class="row" style="margin-left:20%;"> {event.get_html_url}</div>    <div class="row" style="margin-left:20%;"> {event.deleteEvent}</div>  </div> </div></li><div class="modal fade "style="margin-top:13%;" id="desModal2" tabindex="-1" aria-labelledby="desModal2Label" aria-hidden="true"> <div class="modal-dialog"> <div class="modal-content"> <div class="modal-header"><h5 class="modal-title" id="desModalLabel">Event Description</h5></div><div class="modal-body"> <p>{event.get_event_description}</p> </div> <div class="modal-footer"><button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button></div></div></div></div>'
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
	def deleteEvent(self, withyear=True):
		events = Event.objects.filter(date__year=self.year, date__month=self.month)

		events.delete()
		return events

	