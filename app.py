#This is Heroku Deployment Lectre
from flask import Flask, request, render_template
import os
import pickle

print("Test")
print("Test 2")
print(os.getcwd())
path = os.getcwd()

with open('Models/Pickle_DT_Model.pkl', 'rb') as f:
    decision_tree = pickle.load(f)

with open('Models/Pickle_KN_Model.pkl', 'rb') as f:
    k_nearest_neighbour = pickle.load(f)

with open('Models/Pickle_LR_Model.pkl', 'rb') as f:
    logistic_regression = pickle.load(f)


def get_predictions(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, req_model):
    mylist = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
    mylist = [float(i) for i in mylist]
    vals = [mylist]

    if req_model == 'Decision Tree':
        #print(req_model)
        return decision_tree.predict(vals)[0]

    elif req_model == 'K Nearest Neighbour':
        #print(req_model)
        return k_nearest_neighbour.predict(vals)[0]

    elif req_model == 'Logistic Regression':
        #print(req_model)
        return logistic_regression.predict(vals)[0]
    else:
        return "Cannot Predict"


app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def my_form_post():
    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']
        cp = request.form['cp']
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach = request.form['thalach']
        exang = request.form['exang']
        oldpeak = request.form['oldpeak']
        slope = request.form['slope']
        ca = request.form['ca']
        thal = request.form['thal']
        req_model = request.form['req_model']

        target = get_predictions(age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, req_model)

        if target == 1:
            heart_disease = 'Customer is likely to have heart disease'
        else:
            heart_disease = 'Customer is unlikely to have heart disease'

        return render_template('home.html', target=target, heart_disease=heart_disease)
    else:
        return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
