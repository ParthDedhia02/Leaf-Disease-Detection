from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from fileinput import filename
import tensorflow as tf
import os
import numpy as np

app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def predict_image(img_path):
    model = tf.keras.models.load_model('model.h5')
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    # img_np = np.array(img)
    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    return predictions


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# rendering index page
@app.route("/")
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':   
        f = request.files['img']
        # Rerender Index page if no file is selected
        if f.filename == '':
            return render_template("index.html", error="No file selected. Please upload an image file.")

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD'], filename))
            img1 = os.path.join(app.config['UPLOAD'], filename)
            score = predict_image(img1)
            return render_template('import.html',filename=filename, img=img1, score=score)
        else:
            return render_template('index.html', error="Invalid file format. Please upload a valid image file.")
    return render_template('import.html')


if __name__ == '__main__':
    app.run(debug=True)
