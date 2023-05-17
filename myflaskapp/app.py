from flask import Flask, jsonify, request, render_template
from keras.models import load_model
import numpy as np

# Load the trained model
model = load_model('lstm_model.h5', compile=False)
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
timesteps = 1
input_dim = 8

# Initialize the Flask application
app = Flask(__name__)
app.debug = True
@app.route('/')
def home():
    return render_template('index.html')

# Define a route for predicting on new data
@app.route('/predict', methods=['POST'])
def predict():
    max_temp = float(request.form['max_temp'])
    min_temp = float(request.form['min_temp'])
    rel_humidity = float(request.form['rel_humidity'])
    wind = float(request.form['wind'])
    evaporation = float(request.form['evaporation'])
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    radiation = float(request.form['radiation'])

    # Render the result page with the prediction value

    input_data = np.array([max_temp, min_temp, rel_humidity, wind, evaporation, latitude, longitude, radiation])
    input_shape = (1, 1, 9)
    default_value = 0 
    new_input_data = np.full(input_shape, default_value)

    new_input_data[:, :, :8] = input_data 
    prediction = str(model.predict(new_input_data)[0][0])

    #return redirect(url_for('result', prediction=prediction))


    # Render the result page with the prediction value
    return render_template('result.html', prediction=prediction)




if __name__ == '__main__':
    app.run(port=8000)

