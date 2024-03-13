import time
import logging

class Schedule:
    SECONDS_PER_MINUTE = 60
    MINUTES_PER_HOUR = 60
    HOURS_IN_DAY = 24
    DAYS_IN_WEEK = 7

    SECONDS_PER_DAY = HOURS_IN_DAY * MINUTES_PER_HOUR * SECONDS_PER_MINUTE

    def __init__(self, sunday, monday, tuesday, wednesday, thursday, friday, saturday):
        self.logger = logging.getLogger("schedule")
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

    def getNextScheduledTime(self, now=time.time()):
        localTime = time.localtime(now)
        currentSecondsIntoDay = self.secondsIntoDay(time.localtime(now))
        nowDay = localTime.tm_wday

        found = None
        dayFromNow = 0
        secondsAdded = 0

        #
        # Note: loop goes through eight days in case the next chore date
        # is one week from earlier today
        #
        self.logger.debug("Getting next scheduled time from %s" % (time.ctime(now)))
        while found == None and dayFromNow <= Schedule.DAYS_IN_WEEK:
            dayToCheck = ( dayFromNow + nowDay ) % Schedule.DAYS_IN_WEEK
            timeToCheck = currentSecondsIntoDay if dayFromNow == 0 else 0
            self.logger.debug("checking day %d" % (dayFromNow))
            found = self.findNextTime(self.days[dayToCheck],timeToCheck)
            if found == None:
                secondsAdded += Schedule.SECONDS_PER_DAY - timeToCheck
                dayFromNow += 1
            elif dayFromNow == 0:
                found -= currentSecondsIntoDay

        if found != None:
            self.logger.debug("Got %s which is %s with %d seconds added" % (found, time.ctime(found + secondsAdded + now), secondsAdded))
            found += secondsAdded + now
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
