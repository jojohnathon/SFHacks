import datetime
import os.path
import os
import pytz
from datetime import datetime as Datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class CalendarEvent():
    def __init__(self, apikey, creds):
        self.creds = creds
        self.next_time = self.get_next_meeting_time(self.creds)
        self.event = None
        self.realtime = ''
        

    def get_month_days(self, month, year):
        days = 0
        match month:
            case 1 | 3 | 5 | 7 | 8 | 10 | 12:
                days = 31
            case 2:
                if year % 4 == 0:
                    days = 29
                else:
                    days = 28
            case 4 | 6 | 9 | 11:
                days = 30
        return days

    def get_next_meeting_time(self, creds):
        self.event = {'location': 'blank', 'summary': 'blank'}
        try:
            service = build("calendar", "v3", credentials=creds)
            now = datetime.datetime.utcnow().isoformat() + "Z"
            #now = Datetime.now(datetime.timezone.utc).astimezone(tz).isoformat()
            #print(now)
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=1,
                    singleEvents=True,
                    orderBy="startTime",
                    timeZone='UTC'
                )
                .execute()
            )
            events = events_result.get("items", [])
            
            if not events:
                return -1
            for event in events:
                self.event = event
                start = event["start"].get("dateTime", event["start"].get("date"))
                #print(start)
                date = start.split('T')[0]
                year = int(date.split('-')[0])
                month = int(date.split('-')[1])
                day = int(date.split('-')[2])
                
                time = start.split('T')[1]
                hour = int(time.split(':')[0])
                minute = int(time.split(':')[1])
                self.realtime = [year, month, day, hour, minute]
                final_time = minute + (hour * 60) + (day * 24 * 60) + (month * self.get_month_days(month, year) * 24 * 60) + (year * month * self.get_month_days(month, year) * 24 * 60)
                self.next_time = final_time
                
                return final_time
        except HttpError as error:
            print(f"An error occurred: {error}")
            return
        
    def get_event(self):  
        if 'summary' not in self.event:
            self.event['summary'] = 'blank'
        if 'location' not in self.event:
            self.event['location'] = 'blank'
        event_details = [self.event['location'], self.event['summary']]
        return event_details
    
    def get_realtime(self):
        real_time = ''

        # Hour
        am_pm = ''
        if (self.realtime[3] == 0):
            am_pm = 'A.M.'
            real_time = '12:'
        elif (self.realtime[3] < 12):
            am_pm = 'A.M.'
            real_time = str(self.realtime[3]) + ':'
        else:
            am_pm = 'P.M.'
            pm_time = self.realtime[3] - 12
            real_time = str(pm_time) + ':'

        # Minute
        if len(str(self.realtime[4])) == 1:
            real_time += "0" + str(self.realtime[4]) + ' ' + am_pm + " UTC "
        else: 
            real_time += str(self.realtime[4]) + ' ' + am_pm + " UTC "
        # Month
        match str(self.realtime[1]):
            case '1':
                real_time += 'January'
            case '2':
                real_time += 'February'
            case '3':
                real_time += 'March'
            case '4':
                real_time += 'April'
            case '5':
                real_time += 'May'
            case '6':
                real_time += 'June'
            case '7':
                real_time += 'July'
            case '8':
                real_time += 'August'
            case '9':
                real_time += 'September'
            case '10':
                real_time += 'October'
            case '11':
                real_time += 'November'
            case '12':
                real_time += 'December'

        # Day and Year
        if len(str(self.realtime[2])) == 1:
            real_time += " 0" + str(self.realtime[2])
        else:
            real_time += " " + str(self.realtime[2])
        real_time += ", " + str(self.realtime[0])
            

        return real_time
    
    def time_diff(self):
        utc_dt = Datetime.now(datetime.timezone.utc)
        cur_time = utc_dt.astimezone().isoformat('T')
        split2 = cur_time.split('T')[0]
        year2 = int(split2.split('-')[0])
        month2 = int(split2.split('-')[1])
        day2 = int(split2.split('-')[2])

        time2 = cur_time.split('T')[1]
        hour2 = int(time2.split(':')[0])
        minute2 = int(time2.split(':')[1])

        

        final_cur_time = minute2 + (hour2 * 60) + (day2 * 24 * 60) + (month2 * self.get_month_days(month2, year2) * 24 * 60) + (year2 * month2 * self.get_month_days(month2, year2) * 24 * 60)
        print(self.next_time - final_cur_time)
        return self.next_time - final_cur_time
    
        
