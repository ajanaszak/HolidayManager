import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from datetime import date
import json
from dataclasses import dataclass
from dateutil.relativedelta import relativedelta

global holidayClass
global yearSelect
global weekSelect
BigDict = {} # eventually the main dict of names and dates of holidays
BigNameList = [] # temp list to store name values in
BigDateList = [] # temp list to store date values in
# import given json
with open('holidays.json') as f:
    data = json.load(f)
f.close()

# OG print out
def main():
    global holidayClass
    print('Holiday Management 2020 - 2024')
    print('==============================')
    print('There are '+str(len(holidayClass))+' holidays stored in this system across 5 years')
    print()
    Top()

# 'main' menu, come back to this after every action (except exit)
def Top():
    print('Holiday Menu')
    print('============')
    print('1) Add a Holiday')
    print('2) Remove a Holiday')
    print('3) Save Holiday List')
    print('4) View Holidays')
    print('5) Exit')
    print()
    menuOption = input("Please select a menu option, by number, from above: ")
    print()
    while menuOption != 1 or menuOption != 2 or menuOption != 3 or menuOption != 4 or menuOption != 5:
        if menuOption.isnumeric() == False:
            menuOption = input("That is an invalid entry. Please enter a number: ")
        elif int(menuOption) > 5:
            menuOption = input("That is an invalid entry. Please enter a number between 1 and 5: ")
        else:
            break
    print("You have selected option",menuOption,".")
    print()
    if menuOption == '1':
        AddHoliday()
    if menuOption == '2':
        RemoveHoliday()
    if menuOption == '3':
        SaveFile()
    if menuOption == '4':
        ViewHolidays()
    if menuOption == '5':
        prompt2 = input("Are you sure you want to exit? [Y/N] ")
        if prompt2 == 'Y':
            print()
            print("Goodbye!")
            # file.close()
            exit()
        else:
            Top()

def AddHoliday():
    global holidayClass
    global BigDict
    global BigDateList
    global BigNameList
    print('Add a Holiday')
    print('=============')
    inputName = input("Please enter the name of the Holiday you'd like to add to the calendar: ")
    if inputName.isalpha() == "False":
        print("That input is not valid. We were looking for a name. ")
        print()
        AddHoliday()
    BigNameList.append(inputName)
    inputDate = input("Please enter the date (between 2020 - 2024) you'd like to register for this holiday in YYYY-MM-DD format: ")
    if len(inputDate) > 10 or len(inputDate) < 10:
        print("That date is invalid. Please enter a date for the years 2020 - 2024")
        inputDate = input("Please enter the date you'd like to register for this holiday in YYYY-MM-DD format: ")
    BigDateList.append(inputDate)
    for i in range(0,len(BigNameList)):
        BigDict[i] = {}
        BigDict[i]['date'] = BigDateList[i]
        BigDict[i]['name'] = BigNameList[i]
    holidayClass = [None]*len(BigDict)
    for i in range(0,len(BigDict)):
        holidayClass[i] = Holiday(BigDict[i]['name'],BigDict[i]['date'])
    print('Success: ')
    print(inputName+' ('+inputDate+') '+'has been added to the listing.')
    print()
    Top()

def RemoveHoliday():
    global holidayClass
    global BigDateList
    global BigNameList
    global BigDict
    print('Remove a Holiday')
    print('================')
    inputName = input("Please enter the name of the Holiday you'd like to remove from the calendar: ")
    if inputName not in BigNameList:
        print("Error:")
        print("That Holiday does not exist in the registry. ")
        print()
        Top()
    while inputName in BigNameList:
        index = BigNameList.index(inputName)
        BigNameList.pop(index)
        BigDateList.pop(index)
        for i in range(0,len(BigNameList)):
            BigDict[i] = {}
            BigDict[i]['date'] = BigDateList[i]
            BigDict[i]['name'] = BigNameList[i]
        holidayClass = [None]*len(BigDict)
        for i in range(0,len(BigDict)):
            holidayClass[i] = Holiday(BigDict[i]['name'],BigDict[i]['date'])
        print("That holiday has been removed from the registry.")
        print()
        Top()

def ViewHolidays():
    global yearSelect
    global weekSelect
    global holidayClass
    import requests
    weatherURL = "https://api.tomorrow.io/v4/timelines"
    
    print('View Holidays')
    print('=============')
    yearSelect = (input('Which Year? '))
    weekSelect = (input('Which week? [1-52, leave blank for current week]: '))
    print()
    if weekSelect == '':
        weekSelect = 40
    year = int(yearSelect)
    weekNum = int(weekSelect)
    # current week for Oct 4: weekNum =  40
    DateRange = []
    for i in range(1,8):
        x = str(datetime.fromisocalendar(year, weekNum, i))
        DateRange.append(x[:10])
    DateMin = DateRange[0]
    DateMax = DateRange[-1]    
    if weekNum == 40 and year == 2021:
        prompt = input('Would you like to see the weather for this week? [y/n] ')
        if prompt == 'y':
            urlW = "https://api.tomorrow.io/v4/timelines"
            querystring = {
                "location":"44.88535782075044, -93.27795993321281",
                "fields":["temperature", "cloudCover"],
                "units":"imperial",
                "timesteps":"1d",
                "endTime":"2021-10-11T00:00:00Z",
                "apikey":"vCuqHuKcMjIpYmzQ9OdigBp1Pstjvpb3"}
            response = requests.request("GET", urlW, params=querystring)
            print("Weather Forecast")
            print("================")

            results = response.json()['data']['timelines'][0]['intervals']
            results
            
            for daily_result in results:
                date = daily_result['startTime'][0:10]
                temp = round(daily_result['values']['temperature'])
                cloud = round(daily_result['values']['cloudCover'])
                print("On",date,"it will be", temp, "F and there will be", cloud, "percent cloud coverage")
                
        weekDate = filter(lambda x: x in DateRange, BigDateList)
        print()
        print('Holidays This Week')
        print('==================')    
        for i in range(0, len(holidayClass)):
            result = (lambda x, y, z: x >= y and x <= z)(holidayClass[i].date, DateMin, DateMax)
            if result == True:
                print(str(holidayClass[i].name)+' ('+str(holidayClass[i].date)+')')
    else:
        print('Holidays')
        print('========')
        for i in range(0, len(holidayClass)):
            result = (lambda x, y, z: x >= y and x <= z)(holidayClass[i].date, DateMin, DateMax)
            if result == True:
                print(str(holidayClass[i].name)+' ('+str(holidayClass[i].date)+')')
    print()
    Top()

def SaveFile():
    global BigDateList
    global BigNameList
    global BigDict
    global holidayClass
    import os
    prompt = input('Are you sure you want to save your changes? [y/n]: ')
    print()
    if prompt == 'n':
        print('Cancelled:')
        print('Holiday list file save cancelled.')
        print()
        Top()
    else:
        for i in range(0,len(BigNameList)):
            BigDict[i] = {}
            BigDict[i]['date'] = BigDateList[i]
            BigDict[i]['name'] = BigNameList[i]
        holidayClass = [None]*len(BigDict)
        for i in range(0,len(BigDict)):
            holidayClass[i] = Holiday(BigDict[i]['name'],BigDict[i]['date'])
        JSONthing = json.dumps(BigDict)
        fout = open('HolidaysFile.json','r')
        fout = open('HolidaysFile.json','w')
        fout.write(JSONthing)
        fout.close()
        Top()
            
# SCRAAAAAAPE
for i in range(0,5): # loops through years in web
    url = ('https://www.timeanddate.com/holidays/us/202'+str(i))
    soup = BeautifulSoup(requests.get(url).text, 'lxml') # library for processing html and xml

    # scrape
    out = [[td.text.strip() for td in tr.select('th, td')] for tr in soup.select('tr[data-mask]')] # for row in table, strip whitespace from each element
    for item in out: # add 2nd item (name) to main list
        BigNameList.append(item[2])
    year = ', 202'+str(i) # adjusts year value to value in loop
    Stuff = [] # init empty list, will contain dates + year
    
    # adds year value to date that was scraped
    for item in out: 
        Date = item[0] + year
        Stuff.append(Date)
    
    # function to modify format of date
    def mdy_to_ymd(d):
        return datetime.strptime(d, '%b %d, %Y').strftime('%Y-%m-%d')
    
    # adds re-formatted dates to list
    for date in Stuff:
        numDate = mdy_to_ymd(date)
        BigDateList.append(numDate)

# Class assignment chunk, also fixes gt, ge equality statements
@dataclass
class Holiday:
    """Holiday Class"""
    name: str
    date: datetime

    def __gt__(self, other):
        return self.date > other.date

    def __ge__(self, other):
        return self.date >= other.date

    def __str__(self):
        return (self.name + " (" + self.date + ")")

    def __eq__(self, other):
        return (self.name == other.name)

for i in range(0,7):
    BigNameList.append((data['holidays'][i]['name']))
    BigDateList.append((data['holidays'][i]['date']))

for i in range(0,len(BigNameList)):
    BigDict[i] = {}
    BigDict[i]['date'] = BigDateList[i]
    BigDict[i]['name'] = BigNameList[i]

holidayClass = [None]*len(BigDict)
for i in range(0,len(BigDict)):
    holidayClass[i] = Holiday(BigDict[i]['name'],BigDict[i]['date'])




    


###############################

# don't delete this, this time 

# (ノಠ益ಠ)ノ彡┻━┻
main()