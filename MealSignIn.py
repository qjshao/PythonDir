#coding=utf-8
import json
import urllib2
import re
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers import cron, interval


def GetTime():
    return time.strftime('%Y-%m-%d %H:%M:%S   ', time.localtime())

def Heartbeat():
    strOut = GetTime() + "Task Running"
    print strOut

class MealSignIn:
    def __init__(self, user, passward):
        self.user = user
        self.passward = passward

    def get_data_timstamp(self, http_rsp):
        data_pattern = re.compile(r"data:\{timestamp: (\d{13})\},")
        data_match_what = re.search(data_pattern, r"" + http_rsp)
        if 1 == data_match_what.lastindex:
            # print data_match_what.group(1)
            return data_match_what.group(1)
        return ""

    def SignedIn(self):
        # url
        str_url_login = 'http://10.78.13.168/InformationPlatform/home/login'

        # cookies
        login_cookies = urllib2.HTTPCookieProcessor()
        openner = urllib2.build_opener(login_cookies)

        # login
        login_request = urllib2.Request(url=str_url_login,
                                        data='username=' + self.user + '&password=' + self.passward,
                                        headers={'Host':'10.78.13.168',
                                                 'Content-Type': 'application/x-www-form-urlencoded',
                                                 'Referer': 'http://10.78.13.168/InformationPlatform/meal/mark',
                                                 'User-agent': 'Mozilla / 5.0(Windows NT 6.1; WOW64; rv:34.0) Gecko / 20100101 Firefox / 34.0'})
        login_respone = {}
        try:
            login_respone = openner.open(login_request)
        except Exception, e:
            print 'user name error.', e
            return False

        # get timestamp
        url_mark = 'http://10.78.13.168/InformationPlatform/meal/mark'
        mark_request = urllib2.Request(url=url_mark)
        mark_response = openner.open(mark_request)
        # print mark_response.read()
        timestamp_data = self.get_data_timstamp(mark_response.read())

        # signed in
        url_meal_regiest = 'http://10.78.13.168/InformationPlatform/meal/register/'
        regist_meal_request = urllib2.Request(url=url_meal_regiest)
        regist_meal_response = openner.open(regist_meal_request, data='timestamp=' + str(timestamp_data))
        if not (200 == regist_meal_response.code):
            print (GetTime() + 'regist meal failed.' + regist_meal_response.read())
            return
        # print regist_meal_response.read()
        # the result of openner.open can't be read more than one time. or it will be empty
        str_result = regist_meal_response.read()
        json_result = json.loads(str_result)
        print (GetTime() + json_result['msg'])
        # print str_result
        return True


if __name__ == "__main__":

    strUser="shaofeng"
    meal = MealSignIn(strUser, r'..')
    scheduler = BlockingScheduler()

    #    year (int|str) – 4-digit year
    #    month (int|str) – month (1-12)
    #    day (int|str) – day of the (1-31)
    #    week (int|str) – ISO week (1-53)
    #    day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
    #    hour (int|str) – hour (0-23)
    #    minute (int|str) – minute (0-59)
    #    second (int|str) – second (0-59)
    #    start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
    #    end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
    #    timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)
    #
    #    Expression 	Field 	    Description
    #    * 	            any 	    Fire on every value
    #    */a 	        any 	    Fire every a values, starting from the minimum
    #    a-b 	        any 	    Fire on any value within the a-b range (a must be smaller than b)
    #    a-b/c 	        any 	    Fire every c values within the a-b range
    #    xth y 	        day 	    Fire on the x -th occurrence of weekday y within the month
    #    last x 	    day 	    Fire on the last occurrence of weekday x within the month
    #    last 	        day 	    Fire on the last day within the month
    #    x,y,z 	        any 	    Fire on any matching expression; can combine any number of any of the above expressions
    scheduler.add_job(func=meal.SignedIn,
                      name='AutoSigIn',
                      trigger='cron',
                      day_of_week='0-4',
                      hour=18,
                      minute=48)

    scheduler.add_job(func=Heartbeat,
                      name='Heartbeat',
                      trigger='interval',
                      hours=1)

    try:
        print (GetTime() + '[' + strUser + '] Task Begin')
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        print(GetTime() + 'Exit The Job!')



