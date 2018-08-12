from flask import Flask, render_template, send_file
from flask_socketio import SocketIO, emit
from threading import Thread
from ai import image, const
import db
import base64
import re
from io import BytesIO
import datetime
import requests
import pdfkit
from twilio.rest import Client


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aib'
socketio = SocketIO(app)

twilio_client = Client(const.TWILIO_ID, const.TWILIO_TOKEN)

path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

running_threads = 0


def process_image(base64_image, temperature, username, business):
    global running_threads
    converted_image = BytesIO(base64.b64decode(re.sub("data:image/jpeg;base64", '', base64_image)))
    try:
        result = image.ms_api(converted_image)
        if result is not None:
            processed_image, labels = result

            current_time = str(datetime.datetime.now())
            weather = requests.get('https://api.weather.gov/alerts/active/area/NY').json()
            alert = weather['features'][0]['properties']['event']

            buffered = BytesIO()
            processed_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            log = {'time': current_time, 'temperature': temperature, 'alert': alert,
                   'labels': labels,
                   'images': [img_str]}
            db.add_log(username, business, log)
            emit('log', log)
            send_sms('AIB Alert on '+current_time+': '+" ".join(labels))
    except:
        pass
    running_threads -= 1


def send_sms(content):
    message = twilio_client.messages.create(to="+13474595013", from_="+16174058420", body=content)
    print(message)


def demo_user():
    user = db.get_user('mscarn')
    user['username'] = 'mscarn'
    return user


@app.route('/dashboard')
def dashboard():
    user = demo_user()
    return render_template('dashboard.html', user=user, reversed=reversed)


@app.route('/export')
def export():
    pdf = pdfkit.from_url(const.HOSTNAME+'/export/pdf', False, configuration=config)
    return send_file(pdf)


@app.route('/export/pdf')
def export_pdf():
    user = demo_user()
    return render_template('document.html', user=user, reversed=reversed)


@socketio.on('stream')
def stream(data):
    global running_threads
    print(data)
    try:
        username = data['username']
        business = data['business']
        base64_image = data['image']
        temperature = data['temperature']
        img_str = base64_image

        if const.REALTIME_RECOG:
            converted_image = BytesIO(base64.b64decode(re.sub("data:image/jpeg;base64", '', base64_image)))
            img_str = base64_image
            try:
                processed_image, labels = image.process_image(converted_image)

                weather = requests.get('https://api.weather.gov/alerts/active/area/NY').json()
                alert = weather['features'][0]['properties']['event']

                buffered = BytesIO()
                processed_image.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue())
                log = {'time': datetime.datetime.now(), 'temperature': temperature, 'alert': alert, 'labels': labels,
                       'images': [img_str]}
                db.add_log(username, business, log)
                emit('log', log)
            except:
                pass
        elif const.MSFT_API:
            if running_threads < const.MSFT_API_THREADS:
                thread = Thread(target=process_image, args=(base64_image, temperature, username, business))
                thread.start()
                running_threads += 1
        emit('stream', img_str, broadcast=True, include_self=False)
    except Exception as e:
        return {'status': False, 'message': str(e)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
