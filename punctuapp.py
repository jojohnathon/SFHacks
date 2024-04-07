import os.path
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from calendar_app import CalendarEvent
from distanceMatrix import distanceMatrix
import matrixkey
import aiIntegration

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class PunctuApp():
  def __init__(self):
    # initialized once, never changed
    self.creds = ''
    self.distMatrix = distanceMatrix(matrixkey.API_KEY)
    self.login()
    self.calendar = CalendarEvent(matrixkey.API_KEY, self.creds)
    # changed on event refresh
    self.next_event = []
    self.next_time = -1
    self.email = 0
    # changed on 3 hr mark
    self.time_to_dest = -1

    self.refresh_next_event()
    
  def login(self):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      self.creds = creds
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

  def logout(self):
    if os.path.exists('token.json'):
      os.remove('token.json')
      self.creds = None
    else:
      return -1
  def refresh_next_event(self):
    print('REFRESH EVENT')
    self.next_time = self.calendar.get_next_meeting_time(self.creds)
    self.next_event = self.calendar.get_event()
    self.email = aiIntegration.email_TF(self.next_event[1])
  def get_next_time(self):
    return self.next_time
  def get_event_sum(self):
    return self.next_event[1]
  def get_is_email(self):
    return self.email
  def get_destination(self):
    return self.next_event[0]
  
  def update(self):

    if self.calendar.time_diff() <= 180:
      self.time_to_dest = self.distMatrix.get_traffic_time(self.next_event[0])['rows'][0]['elements'][0]['duration']['value'] / 60
      #print('U HAVE MEETING STOOPID')
      # stuff to notify user of imminent meeting
    if self.calendar.time_diff() <= 0:
      self.refresh_next_event()
      print(self.get_is_email())

if __name__ == '__main__':
  app = PunctuApp()

  loop = True
  while(loop):
    app.update()