from typing import List
import datetime
days_code = {
    "LUN": 0,
    "MAR": 1,
    "MER": 2,
    "GIO": 3,
    "VEN": 4,
}

def next_weekday(d: datetime.date, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_free_slots(hours: List[datetime.datetime], appointments: List[List[datetime.datetime]], duration=datetime.timedelta(minutes=30)) -> List[str]:
    # https://stackoverflow.com/questions/10702224/python-algorithm-find-time-slots
    slots = sorted([(hours[0], hours[0])] + appointments + [(hours[1], hours[1])])
    free = []
    for start, end in ((slots[i][1], slots[i+1][0]) for i in range(len(slots)-1)):
        assert start <= end, "Cannot attend all appointments"
        while start + duration <= end:
            free.append(start.strftime("%H:%M"))
            start += duration
    return free