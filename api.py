from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from ai import image
import db
import base64
import re
from io import BytesIO
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aib'
socketio = SocketIO(app)


@app.route('/dashboard')
def dashboard():
    user = db.get_user('mscarn')
    user['username'] = 'mscarn'
    return render_template('dashboard.html', user=user)


@socketio.on('stream')
def stream(data):
    try:
        username = data['username']
        business = data['business']
        base64_image = data['image']
        temperature = data['temperature']
        converted_image = BytesIO(base64.b64decode(re.sub("data:image/jpeg;base64", '', base64_image)))

        img_str = base64_image
        try:
            processed_image, labels = image.process_image(converted_image)
            buffered = BytesIO()
            processed_image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            log = {'time': datetime.datetime.now(), 'temperature': temperature, 'labels': labels, 'images': [img_str]}
            db.add_log(username, business, log)
            emit('log', log)
        except:
            pass
        emit('stream', img_str, broadcast=True, include_self=False)
    except Exception as e:
        return {'status': False, 'message': str(e)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
