# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request, redirect
import time
from datetime import datetime, timedelta, date
import threading
import signal
import sys
import json

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC7606568450382565cf9093d862dc94aa"
auth_token = "a4814a157c52a03618d3a0419a2e7eed"
client = Client(account_sid, auth_token)

def signal_handler(signal, frame):
  print("parent process terminated")
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def check_reminder():
  today = date.today()
  print("Today's date:", today)
  now = datetime.now()
  print(now)


def send_message(message_text):
  message = client.messages.create(
  body="Reminder to take your medication",
  from_="12765660767",
  to="+13303109914"
)
  print(message.sid)

app = Flask(__name__)
@app.route("/sms", methods = ["GET", "POST"])
def sms():
  resp = MessagingResponse()
  body = request.form['Body']
  message_body = request.form['Body']
  #print('Received message: {}'.format(message_body))
  message_sender = request.form['From']
  #print('message from: {}'.format(message_sender))
  with open("messages.txt", 'a') as f:
    f.write(message_body)
    f.close()

  return("All Good")


def run_app():
   app.run(debug=True, use_reloader = False)

def read_message():
  message=None
  try:
    with open("messages.txt", 'r+') as f:
      line = None
      i = 0
      for line in f.readlines():
        message=line
      f.close()
  except:
    pass
  return(message)


def main():
  f = open("messages.txt", 'w')         #open and close message file to clear data and make sure permissions are correct
  f.close
  flask_thread = threading.Thread(target=run_app)
  flask_thread.start()
  #print(app.run(debug="True"))
  while(1):
    time.sleep(3)
    current_time=datetime.now()
    print("current_time: ", (current_time.hour))
    message=read_message()
    if(message!=None):
      send_time=int(message)
      print("send time:", send_time)
      if((current_time.hour)>send_time):
        send_message(message)
        send_time=send_time+24
        return
    
main()
