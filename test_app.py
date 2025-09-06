import pytest
from unittest.mock import patch, MagicMock
from app import app

# Cria um client de teste do Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# envia requisição POST com JSON com mensagem qualquer
@patch("app.get_llm_response")
def test_any_message(mock_llm, client):
    # Simula resposta do LLM
    mock_llm.return_value ='{"clima":0,"cidade":"","resposta":"Olá, humano!"}'
    
    response = client.post("/", json={"message": "Responda exatamente: 'Olá, humano!'"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["response"] == 'Olá, humano!'


# Envia requisição POST com JSON com mensagem sobre tempo
@patch("app.get_weather")
@patch("app.get_llm_response")
def test_weather_message(mock_llm, mock_weather, client):
    # Simula resposta do LLM
    mock_llm.return_value = '{"clima":1,"cidade":"Rio de Janeiro","resposta":"ok"}'

    # Simula resposta da WeatherAPI
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "forecast": {
            "forecastday": [
                {},  
                {"day": {"maxtemp_c": 30.2, "mintemp_c": 20.4}} 
            ]
        }
    }
    mock_weather.return_value = fake_response

    response = client.post("/", json={"message": "Como está o tempo no Rio de Janeiro?"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["response"] == f'A previsão do tempo em Rio de Janeiro amanhã é de mínima 20 e máxima 30 graus.'


# Envia requisição POST com JSON com mensagem sobre tempo em local inexistente
@patch("app.get_weather")
@patch("app.get_llm_response")
def test_weather_non_existent_place(mock_llm, mock_weather, client):
    # Simula resposta do LLM
    mock_llm.return_value = '{"clima":1,"cidade":"Lalaland","resposta":"ok"}'

    # Simula resposta da WeatherAPI
    fake_response = MagicMock()
    fake_response.status_code = 400
    fake_response.json.return_value = {
        "error": {
        "code": 1006,
        "message": "No matching location found."
        }
    }
    mock_weather.return_value = fake_response

    response = client.post("/", json={"message": "Como está o tempo em Lalaland?"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["response"] == 'Desculpe, não foi possível encontrar informações sobre o tempo em Lalaland'


# Envia JSON vazio
def test_empty_json(client):
    response = client.post("/", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["response"] == "Mensagem não fornecida"