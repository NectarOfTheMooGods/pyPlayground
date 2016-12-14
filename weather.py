#! /usr/bin/python3
#
# weather.py - prints weather from Poway

import sys, os
import json, requests
import pprint
import calendar
import datetime

#local modules
import debugger



def RequestWeatherData(url):
    try:
        # download the JSON data from OpenWeatherMap.org
        response = requests.get(url)
        response.raise_for_status()
    except:
        print( "error with request" )
        sys.exit(-1)

    data = json.loads(response.text)
    #pprint.pprint(data)
        
    return data


def KelvinToFahrenheit(k):
    return (k*9/5.0)-459.67


def main(argv):
    #debugger.attachDebugger()

    numDays = 7
    degreeSign = '\u00b0'
    percentSign = '\u0025'

    site = 'http://api.openweathermap.org/data/2.5/'
    current = 'weather?'
    forecast = 'forecast/daily?'
    city = 'id=5384690&'
    length = 'cnt=%s&' %(numDays)
    appID = 'APPID=63a3b02da3da17793691ad1e43c17fb4'

    url = site + current + city + appID
    weatherData = RequestWeatherData(url)

    print("Current weather for %s:" %(weatherData['name']))
    curTemp = KelvinToFahrenheit(weatherData['main']['temp'])
    humidity = weatherData['main']['humidity']
    #desc = weatherData['weather'][0]['main'] + " - " + weatherData['weather'][0]['description']
    desc = weatherData['weather'][0]['description']
    print("%.1f%s %s%s humidity  %s" %(curTemp, degreeSign, humidity, percentSign, desc))
    

    url = site + forecast + city + length + appID
    weatherData = RequestWeatherData(url)

    print("%s Day Forecast:" %(numDays))

    # build the date strings, with "today" and "tomorrow" for the first 2 slots
    dateStr = ['Today','Tomorrow']
    today = datetime.date.today()
    for i in range(2,numDays):
        newDate = today + datetime.timedelta(days=i)
        dateStr.append(calendar.day_name[newDate.weekday()])

    #zip allows to iterate though 2 lists in tandem
    for date, w in zip(dateStr, weatherData['list']):
        #desc = w['weather'][0]['main'] + " - " + w['weather'][0]['description']
        desc = w['weather'][0]['description']
        hi = KelvinToFahrenheit(w['temp']['max'])
        low = KelvinToFahrenheit(w['temp']['min'])
        date = date.ljust(10)
        print("%s: Hi: %.1f%s Low: %.1f%s   %s" %(date, hi, degreeSign, low, degreeSign, desc))


if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        print("main KeyboardInterrupt")
        pass
