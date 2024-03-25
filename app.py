from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from fileinput import filename
import tensorflow as tf
import os
from PIL import Image

app = Flask(__name__)
class_name=['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']

upload_folder = os.path.join('static', 'uploads')
app.config['UPLOAD'] = upload_folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
classes = ['Early blight', 'Late blight', 'healthy']

# Function to predict the class of the image
def predict_image(img_path):
    model = tf.keras.models.load_model('model.h5')
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = model.predict(img_array)
    print(predictions)
    if predictions.max() in predictions[0]:
        class_name = classes[predictions.argmax()]
        score1 = round((predictions[0][0] * 100),2)
        score2 = round((predictions[0][1] * 100),2)
        score3 = round((predictions[0][2] * 100),2)
        print(class_name)
    return class_name, score1, score2, score3

# Function to copy an image from the source path to the destination path
def copy_image(source_path):
    try:
        # Open the source image
        source_image = Image.open(source_path)
        
        # Create a copy of the source image
        copied_image = source_image.copy()
        
        # Save the copied image to the destination path
        copied_image.save("./static/uploads/copied_image.jpg")
        
        return True  # Return True if copying was successful
    except Exception as e:
        print(f"Error: {e}")
        return False  # Return False if an error occurred

# Function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# rendering index page
@app.route("/")
def index():
    return render_template("index.html")

# rendering the import page
@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':   
        f = request.files['img']
        # Rerender Index page if no file is selected
        if f.filename == '':
            return render_template("index.html", error="Error: No file selected. Please upload an image file.")

        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD'], filename))
            img1 = os.path.join(app.config['UPLOAD'], filename)
            # Example usage
            source_path = img1
            if copy_image(source_path):
                print("Image copied successfully!")
            else:
                print("Failed to copy image.")

            Class, score1, score2, score3 = predict_image(img1)
            img_print = os.path.join(app.config['UPLOAD'], 'copied_image.jpg')
            os.remove(img1)
            return render_template('import.html', img=img_print, Class = Class, score1=score1, score2=score2, score3=score3)
        else:
            return render_template('index.html', error="Error: Invalid file format. Please upload a valid image file.")
    


if __name__ == '__main__':
    app.run(debug=True)
