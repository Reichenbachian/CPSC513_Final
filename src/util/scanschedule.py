import time

from util.repeat import Repeat
from datetime import datetime

class ScanSchedule(object):
    def __init__(self, year, month, day, hour, minute, ampm, repeat):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        hour = int(hour)

        if ((ampm == 'AM' and hour != 12) or (ampm == 'PM' and hour == 12)):
            self.hour = hour
        elif (ampm == "AM" and hour == 12):
            self.hour = 0
        else:
            self.hour = hour + 12

        self.minute = int(minute)
        self.repeat = repeat
    
    def next_schedule(self):
        if (self.repeat == Repeat.ONCE):
            return False
        elif(self.repeat == Repeat.DAILY):
            self._incr_day()
        elif(self.repeat == Repeat.WEEKLY):
            for _ in range(7):
                self._incr_day()
        elif(self.repeat == Repeat.MONTHLY):
            self.month += 1
            if (self.month == 13):
                self.month = 1
                self.year += 1
            if (self.day == 31 and (self.month == 9 or self.month == 4 or self.month == 6 or self.month == 11)):
                self.day = 30
        return True
    
    def wait(self):
        diff = datetime.now() - datetime(self.year, self.month, self.day, self.hour, self.minute)
        diff_seconds = diff.total_seconds()
        if (diff_seconds <= 0):
            return
        else:
            time.sleep(diff_seconds)
            return
    
    def is_past(self):
        now = datetime.now()
        now_sced = ScanSchedule(now.year, now.month, now.day, int(now.strftime("%I")), int(now.strftime("%M")), now.strftime("%p"), Repeat.ONCE)
        if (now_sced < self):
            return False
        else:
            return True
    
    def _incr_day(self):
        self.day += 1
        if (self.day == 31 and (self.month == 9 or self.month == 4 or self.month == 6 or self.month == 11)):
            self.day = 1
            self.month += 1
        elif (self.day == 32):
            self.day = 1
            self.month += 1
            if (self.month == 13):
                self.month = 1
                self.year += 1

    def __eq__(self, other):
        if (self.year == other.year and self.month == other.month and self.day == other.day and self.hour == other.hour and self.minute == other.minute and self.repeat == other.repeat):
            return True
        else:
            return False
    
    def __lt__(self, other):
        if (self.year < other.year):
            return True
        elif (self.year > other.year):
            return False

        if (self.month < other.month):
            return True
        elif (self.month > other.month):
            return False
        
        if (self.day < other.day):
            return True
        elif (self.day > other.day):
            return False
        
        if (self.hour < other.hour):
            return True
        elif (self.hour > other.hour):
            return False

        if (self.minute < other.minute):
            return True
        elif (self.minute > other.minute):
            return False
        
        if (self.repeat < other.repeat):
            return True
        elif (self.repeat > other.repeat):
            return False

        return False
    
    def __str__(self):
        r = None
        if (self.repeat == Repeat.ONCE):
            r = "ONCE"
        elif (self.repeat == Repeat.DAILY):
            r = "DAILY"
        elif (self.repeat == Repeat.WEEKLY):
            r = "WEEKLY"
        elif (self.repeat == Repeat.MONTHLY):
            r = "MONTHLY"

        return f"{self.year:04}-{self.month:02}-{self.day:02} {self.hour:02}:{self.minute:02} [{r}]"
    
    def __repr__(self):
        return self.__str__()