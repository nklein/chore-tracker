import time

class Schedule:
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_IN_DAY = 24
    DAYS_IN_WEEK = 7

    def __init__(self, sunday, monday, tuesday, wednesday, thursday, friday, saturday):
        self.days = [
            self.parseDay(monday),
            self.parseDay(tuesday),
            self.parseDay(wednesday),
            self.parseDay(thursday),
            self.parseDay(friday),
            self.parseDay(saturday),
            self.parseDay(sunday)
        ]
        pass

    def getSecondsUntilNextScheduledTime(self, now=time.localtime()):
        currentSecondsIntoDay = self.secondsIntoDay(now)
        nowDay = now.tm_wday

        found = None
        dayFromNow = 0
        while found == None and dayFromNow < Schedule.DAYS_IN_WEEK:
            dayToCheck = ( dayFromNow + nowDay ) % Schedule.DAYS_IN_WEEK
            timeToCheck = currentSecondsIntoDay if dayFromNow == 0 else 0
            found = self.findNextTime(self.days[dayToCheck],timeToCheck)
            dayFromNow += 1

        if found != None:
            found += dayFromNow * Schedule.HOURS_IN_DAY * Schedule.MINUTES_PER_HOUR * Schedule.SECONDS_PER_MINUTE
            found -= currentSecondsIntoDay

        return found

    def parseDay(self,day):
        times = [ self.parseTime(x) for x in day ]
        return sorted(times)

    def parseTime(self,timeStr):
        return self.secondsIntoDay( time.strptime(timeStr, "%H:%M") )

    def secondsIntoDay(self,ts):
        return ( ts.tm_hour * Schedule.MINUTES_PER_HOUR + ts.tm_min ) * Schedule.SECONDS_PER_MINUTE + ts.tm_sec

    def findNextTime(self, day, timeToCheck):
        index = 0
        while index < len(day) and day[index] < timeToCheck:
            index += 1
        if index < len(day):
            return day[index]
        else:
            return None
