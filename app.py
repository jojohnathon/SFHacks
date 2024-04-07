from flask import Flask, render_template, url_for, request, redirect
from punctuapp import PunctuApp
import os
app = Flask(__name__)
punct = PunctuApp()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and not (os.path.exists('token.json')):
        punct.login()
    elif (os.path.exists('token.json')):
        punct.login()
        return redirect('/dashboard')
    else:
        return render_template('index.html')
    
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if request.method == 'POST':
        if request.form['logout'] == 'Log out':
            punct.logout()
            return redirect('/')
    elif punct.calendar.time_diff() - 420 <= 180:
        return redirect('/event_soon')
    else: 
        print(punct.calendar.time_diff())
        return render_template('dashboard.html', 
                               event1_desc = punct.get_event()[1], 
                               event1_loc = punct.get_event()[0],
                               event1_time = punct.get_realtime(),
                               email = 'This meeting could\'ve been an email' if punct.get_is_email() == 1 else ''
                               )
@app.route('/event_soon', methods=['POST', 'GET'])
def event_soon():
    if request.method == 'POST':
        if request.form['logout'] == 'Log out':
            punct.logout()
            return redirect('/')
    elif punct.calendar.time_diff() - 420 > 180:
        return redirect('/dashboard')
    else: 
        time_to_dest = punct.distMatrix.get_traffic_time(punct.next_event[0])['rows'][0]['elements'][0]['duration']['value'] / 60
        return render_template('event_soon.html', 
                               event1_desc = punct.get_event()[1], 
                               event1_loc = punct.get_event()[0],
                               event1_time = punct.get_realtime(),
                               event1_travel = abs(punct.calendar.time_diff() - 420 - time_to_dest),
                               email = 'This meeting could\'ve been an email' if punct.get_is_email() == 1 else ''
                               )
    

if __name__ == '__main__':
    app.run(debug=True)