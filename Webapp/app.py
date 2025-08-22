#import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import os
from feature_extraction import extract_features


#Initialize the flask App
app = Flask(__name__)
model = joblib.load('forest.pkl')


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'dll', 'exe'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



#default page of our web-app
@app.route('/')
def landing():
    return render_template('landing.html')





@app.route('/signup',methods=['POST'])
def signup():
    if request.method == 'POST':
        return render_template('signup.html')

@app.route('/signupsuccess',methods=['POST'])
def signupsuccess():
    if request.method == 'POST':
        credentials = [(x) for x in request.form.values()]
        print(credentials)
        username = credentials[0]
        password = credentials[1]
        print(type(username))

        file = open("Username/username.txt", "w")
        a = file.write(username)
        file.close()

        file = open("Password/password.txt", "w")
        a = file.write(password)
        file.close()
        return render_template('signupsuccess.html')




@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        return render_template('login.html')



@app.route('/home',methods=['POST'])
def home():
    if request.method == 'POST':
        lcredentials = [(x) for x in request.form.values()]
        print(lcredentials)
        lusername = lcredentials[0]
        lpassword = lcredentials[1]
        print(type(lusername))

        f = open("Username/username.txt", "r")
        username = f.read()
        f = open("Password/password.txt", "r")
        password = f.read()
        print(lusername, username, lpassword, password)

        if username==lusername and password==lpassword:
            print('match')
            template = 'home.html'
        elif username!=lusername or password!=lpassword:
            print('No')
            template = 'loginfail.html'

        return render_template(template)



@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file is uploaded
    if 'file' in request.files:
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return render_template('index.html', error="Unsupported file type.")
        
        # Construct the full file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

        # Save the file
        file.save(file_path)

        # Use the model for prediction if the file is `.exe` or `.dll`
        if allowed_file(file.filename):
            features = extract_features(file_path)  # Your feature extraction function
            prediction = model.predict(features)     # Predict using your model
            result = {
                "type": "file",
                "prediction": "Malware" if prediction[0] == 1 else "Safe",
                "file_name": file.filename
            }

        return render_template('output.html', result=result)

    return render_template('home.html', error="No file uploaded.")






    return render_template('output.html', prediction_text='{}'.format(out))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
