from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import watering_functions
import os
import matplotlib
matplotlib.use('Agg')

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
    watering_functions.generate_moisture_graph()
    return render_template('index.html', **templateData)

@app.route('/last_watered')
def check_last_watered():
    last_watered = watering_functions.get_last_watered()
    message = f"Last watered on: {last_watered}"
    templateData = template(text=message)
    watering_functions.generate_moisture_graph()
    return render_template('index.html', **templateData)

@app.route('/reservoir_empty')
def is_reservoir_empty():
    status = watering_functions.check_reservoir_empty()
    if status == False:
        message = "Water reservoir should still be sufficiently full"
    if status == True:
        message = """
            Something might be wrong with the calibration of the sensor, or the water reservoir might be empty. 
            Either refill the reservoir (and be careful with the wiring :), or contact Axel.
            """
    templateData = template(text=message)
    return render_template('index.html', **templateData)

@app.route('/moisture_level')
def check_moisture_level():
    moisture_level = watering_functions.get_moisture_level()
    templateData = template(text=f'Last measured moisture level was: {moisture_level}')
    return render_template('index.html', **templateData)

@app.route('/water_plant')
def water_plant():
    watering_functions.give_water()
    templateData = template(text="The plant has been watered succesfully.")
    return render_template('index.html', **templateData)


@app.route('/update_moisture_threshold', methods=['POST'])
def update_moisture_threshold():
    if request.method == 'POST':
        form_value = request.form["moisture_threshold"]
        threshold = float(form_value)
        watering_functions.set_moisture_threshold(level=threshold)
        templateData = template(text=f"Moisture threshold has been updated to {threshold}")
        return render_template('index.html', **templateData)
    else:
        templateData = template(text="Error in updating the moisture threshold")
        return render_template('index.html', **templateData)

@app.route('/system_shutdown')
def watering_system_shutdown():
    message = """Watering system will be powered off. To restart, pull the micro USB cable out 
    of the Raspberry Pi and plug it back in after a few seconds."""
    templateData = template(text=message)
    os.system('sudo pkill -f auto_watering.py')
    return render_template('index.html', **templateData)

@app.route('/system_reboot')
def watering_system_reboot():
    message = "Watering system will be rebooted after one minute. Please wait a few seconds for it to restart."
    templateData = template(text=message)
    os.system('sudo shutdown -r 1')
    return render_template('index.html', **templateData)
    
@app.route('/send_test_email')
def send_test():
    watering_functions.send_reminder()
    message = "Test email has been sent to victoria.plas@icloud.com."
    templateData = template(text=message)
    return render_template('index.html', **templateData)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)