import datetime
from datetime import datetime as Datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class CalendarEvent():
    def __init__(self):
        self.next_time = 0

    def get_month_days(month, year):
        days = 0
        match month:
            case 1 | 3 | 5 | 7 | 8 | 10 | 12:
                days = 31
            case 2:
                if year % 4 == 0:
                    days = 29
                else:
                    days = 28
            case 4 | 60 | 9 | 11:
                days = 30
        return days

    def get_next_meeting_time(self, creds):
        try:
            service = build("calendar", "v3", credentials=creds)
            now = Datetime.utcnow().isoformat() + "Z"
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=1,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                return -1
            for event in events:
                self.event = event
                start = event["start"].get("dateTime", event["start"].get("date"))
                date = start.split('T')[0]
                year = int(date.split('-')[0])
                month = int(date.split('-')[1])
                day = int(date.split('-')[2])
                
                time = start.split('T')[1]
                hour = int(time.split(':')[0])
                minute = int(time.split(':')[1])

                final_time = minute + (hour * 60) + (day * 24 * 60) + (month * self.get_month_days(month, year) * 24 * 60) + (year * self.get_month_days(month, year) * 24 * 60 * 365)
                self.next_time = final_time
                return final_time
        except HttpError as error:
            print(f"An error occurred: {error}")
            return
        
    def get_event(self):  
        utc_dt = Datetime.now(datetime.timezone.utc)
        cur_time = utc_dt.astimezone().isoformat('T')
        split2 = cur_time.split('T')[0]
        year2 = int(split2.split('-')[0])
        month2 = int(split2.split('-')[1])
        day2 = int(split2.split('-')[2])

        time2 = cur_time.split('T')[1]
        hour2 = int(time2.split(':')[0])
        minute2 = int(time2.split(':')[1])

        final_cur_time = minute2 + (hour2 * 60) + (day2 * 24 * 60) + (month2 * self.get_month_days(month2, year2) * 24 * 60) + (year2 * self.get_month_days(month2, year2) * 24 * 60)

        if 'summary' not in self.event:
            self.event['summary'] = 'blank'
        event_details = [final_cur_time, self.event['location'], self.event['summary']]
        return event_details

        
