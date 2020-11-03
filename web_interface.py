from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import auto_watering
import os

# Initializes flask based on the name of the file
app = Flask(__name__)

def template(title="", text=""):
    timeString = datetime.now().strftime("%A %d %B %Y at %H:%M:%S")
    templateData = {
        'title' : title,
        'time' : timeString,
        'text' : text
        }
    return templateData

@app.route('/')
def index():
    templateData = template(title='Current time is')
    return render_template('index.html', **templateData)

@app.route('/last_watered')
def check_last_watered():
    last_watered = watering_functions.get_last_watered()
    templateData = template(text=f'Last watered at: {last_watered}')
    return render_template('index.html', **templateData)

@app.route('/reservoir_empty')
def is_reservoir_empty():
    status = watering_functions.check_reservoir_empty()
    if status == False:
        message = "Water reservoir should still be sufficiently full"
    if status == True:
        message = "Water reservoir is empty, please refill it (and be careful with the wiring :)"
    templateData = template(text=message)
    return render_template('index.html', **templateData)

@app.route('/moisture_level')
def check_moisture_level():
    moisture_level = watering_functions.get_moisture_level()
    templateData = template(text=f'Moisture level is currently at: {moisture_level}')
    return render_template('index.html', **templateData)

@app.route('/water_plant')
def water_plant():
    watering_functions.give_water()
    templateData = template(text="The plant has been watered succesfully.")
    return render_template('index.html', **templateData)


@app.route('/update_moisture_threshold', methods=['POST', 'GET'])
def update_moisture_threshold():
    threshold = request.form.get("moisture threshold")
    watering_functions.set_moisture_threshold(threshold)
    templateData = template(text=f"Moisture threshold has been updated to {threshold}")
    return render_template('index.html', **templateData)

@app.route('/system_shutdown/<toggle>')
def watering_system_shutdown(toggle):
    if toggle == "ON":
        print('Watering system will be powered off. To restart, pull the micro USB cable out of the Pi out and plug it back in after a few seconds.')
        os.system('pkill -f auto_watering.py') # filename might need to be changed
    else:
        pass
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)