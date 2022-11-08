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


    #Inputting bad parameters (out of range)
    badParamUrl = '/predict?G1=5&G2=30&absences=100&studytime=3&failures=3'
    response = client.get(badParamUrl)
    assert response.status_code == 400


    #Inputting bad parameters (missing parameter)
    missingUrl = '/predict?G1=9&G2=10&absences=20&studytime=3'
    response = client.get(missingUrl)
    assert response.status_code == 400
    

    #Inputting misspelled parameters
    wrongURL = '/predict?K1=19&K2=19absences=10&studytime=3&failures=3'
    response = client.get(wrongURL)
    assert response.status_code == 400
    


    #Inputting good parameters, smart student
    goodURL = '/predict?G1=20&G2=20&absences=1&studytime=4&failures=0'
    response = client.get(goodURL)
    assert response.status_code == 200
    assert int(response.get_data()) == 1

    #Inputting good parameters, bad student
    goodURL = '/predict?G1=1&G2=1&absences=55&studytime=2&failures=3'
    response = client.get(goodURL)
    assert response.status_code == 200
    assert int(response.get_data()) == 0


