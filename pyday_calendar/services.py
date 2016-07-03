from pyday.settings import DAY, FORMAT_DATE
import calendar
from datetime import datetime
from pyday_calendar.models import Event


def make_hourly_events(events, max_columns):
    # табличка с часовете
    # в кой час кой евент е

    hourly_events = [[None for i in range(max_columns)] for i in range(DAY)]

    for event in events:
        column = (hourly_events[event.from_time - 1]).index(None)
        hourly_events[event.from_time - 1][column] = event
        for i in range(event.from_time, event.to_time - 1):
            hourly_events[i][column] = event
    return hourly_events


def find_max_columns(events):
    hours_events = [0 for i in range(DAY)]
    for event in events:
        for i in range(event.from_time - 1, event.to_time):
            hours_events[i] += 1
    return max(hours_events)


def make_calendar(date):
    date_object = datetime.strptime(date, FORMAT_DATE)
    calendar_obj = calendar.Calendar().monthdayscalendar(date_object.year, date_object.month)
    return [[x if x != 0 else '' for x in week] for week in calendar_obj], date_object.month

