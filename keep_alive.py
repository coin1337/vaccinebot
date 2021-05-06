# This is NOT part of the bot's functionality. This code is meant to create a web server for the bot so it can always stay online.

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
  return "Working."

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()
