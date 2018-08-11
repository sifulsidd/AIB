from flask import Flask, render_template
from flask_socketio import SocketIO
from ai import image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aib'
socketio = SocketIO(app)


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/api/stream', methods=['POST'])
def stream():
    # get image data

    # convert image data

    # process converted image
    new_image, labels = image.process_image(image)

    # convert image

    # send image
