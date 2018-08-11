from flask import Flask, render_template
from flask_socketio import SocketIO
from ai import image
import base64
from io import BytesIO

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
