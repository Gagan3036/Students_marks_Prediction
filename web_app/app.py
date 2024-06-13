from flask import Flask, render_template, request
import joblib as jl
import numpy as np

app = Flask(__name__)

# Load the new trained model
loaded_model = jl.load('students_marks_prediction_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input values from the form
    quiz_01 = float(request.form['quiz_01'])
    quiz_02 = float(request.form['quiz_02'])
    quiz_avg = (quiz_01 + quiz_02) / 2

    ass_01 = float(request.form['ass_01'])
    ass_02 = float(request.form['ass_02'])
    ass_avg = (ass_01 + ass_02) / 2

    Mid_Term = float(request.form['Mid_Term'])

    Final_Marks = quiz_avg + ass_avg + Mid_Term

    # Make prediction using the loaded model
    prediction = loaded_model.predict(np.array([[quiz_01, quiz_02, quiz_avg, ass_01, ass_02 , ass_avg, Mid_Term, Final_Marks]]))

    # Round the prediction to two decimal places
    prediction = round(prediction[0], 2)

    return render_template('index.html', prediction_text=f'Predicted Midterm Marks: {prediction}')

if __name__ == '__main__':
    app.run(debug=True)
