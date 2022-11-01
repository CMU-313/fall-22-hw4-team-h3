from flask import Flask

from app.handlers.routes import configure_routes


def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data() == b'try the predict route it is great!'

def test_predict_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    
    #without inputting parameters
    emptyUrl = '/predict'
    response = client.get(emptyUrl)
    assert response.status_code == 400
    assert response.get_data() == b'Inputs not found!'

    #Inputting bad parameters (out of range)
    badParamUrl = '/predict?G1=5&G2=30&absences=100&studytime=3&failures=3'
    response = client.get(badParamUrl)
    assert response.status_code == 400
    assert response.get_data() == b'Invalid Input: Out of Range'

    #Inputting bad parameters (missing parameter)
    missingUrl = '/predict?G1=9&G2=10&absences=20&studytime=3'
    response = client.get(missingUrl)
    assert response.status_code == 400
    assert response.get_data() == b'Invalid Input: Missing Input'

    #Inputting good parameters 
    goodURL = '/predict?G1=19&G2=15&absences=10&studytime=3&failures=3'
    response = client.get(goodURL)
    assert response.status_code == 200
    assert response.get_data() == b'Applicant is likely to succeed!' or response.get_data() == b'Applicant is not likely to succeed!'

    #Inputting in wrong order
    orderURL = '/predict?G2=19&G1=15&absences=10&studytime=3&failures=3'
    response = client.get(orderURL)
    assert response.status_code == 400
    assert response.get_data() == b'Invalid Input'

    #Inputting repetitive parameters
    repetitiveURL = '/predict?G1=19&G1=15&G2=19absences=10&studytime=3&failures=3'
    response = client.get(repetitiveURL)
    assert response.status_code == 400
    assert response.get_data() == b'Invalid Input'

    #Inputting misspelled parameters
    wrongURL = '/predict?K1=19&K2=19absences=10&studytime=3&failures=3'
    response = client.get(wrongURL)
    assert response.status_code == 400
    assert response.get_data() == b'Invalid Input'

def test_metrics_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/metrics'

    response = client.get(url)

    assert response.status_code == 200
    assert response.get_data()
    assert float(response.get_data()) > 0
    assert float(response.get_data()) < 1