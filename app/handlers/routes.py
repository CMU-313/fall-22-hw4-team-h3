import this
from flask import Flask, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"


    @app.route('/predict')
    def predict():

        #use entries from the query string here but could also use json
        G1 = request.args.get('G1')
        G2 = request.args.get('G2')
        absences = request.args.get('absences')
        studytime = request.args.get('studytime')
        failures = request.args.get('failures')

    

        if not G1 or not G2 or not absences or not studytime or not failures:
            return 'Missing Input', 400
        if((int(G1) < 0) or (int(G1) > 20)):
            return 'Invalid Input', 400
        if((int(G2) < 0) or (int(G2) > 20)):
            return 'Invalid Input', 400
        if((int(absences) < 0) or (int(absences) > 93)):
            return 'Invalid Input', 400
        if((int(studytime) < 0) or (int(studytime) > 4)):
            return 'Invalid Input', 400
        if((int(failures) < 0) or (int(failures) > 4)):
            return 'Invalid Input', 400

        data = [[G1], [G2], [absences], [studytime], [failures]]

        query_df = pd.DataFrame({
            'G1': pd.Series(G1),
            'G2': pd.Series(G2),
            'absences': pd.Series(absences),
            'studytime': pd.Series(studytime),
            'failures': pd.Series(failures)
        })
        
        #query = pd.get_dummies(query_df)

        prediction = clf.predict(query_df)
        return jsonify(np.ndarray.item(prediction))

    @app.route('/metrics')
    def metrics():
        # TO BE IMPLEMENTED
        return "to be implemented"