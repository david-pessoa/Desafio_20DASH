import pytest
from unittest.mock import patch
from app import app

# Cria um client de teste do Flask
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# envia requisição POST com JSON com mensagem qualquer
def test_any_message(client):
    response = client.post("/", json={"message": "Responda exatamente: 'Olá, humano!'"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["response"] == 'Olá, humano!'

# envia requisição POST com JSON com mensagem sobre tempo
def test_weather_message(client):
    response = client.post("/", json={"message": "Como está o tempo no Rio de Janeiro?"})
    assert response.status_code == 200
    data = response.get_json()
    max_temp =  data["response"].split(' ')[-2]
    min_temp =  data["response"].split(' ')[-5]

    assert max_temp >= min_temp
    assert data["response"] == f'A previsão do tempo em Rio de Janeiro amanhã é de mínima {min_temp} e máxima {max_temp} graus.'

# envia requisição POST com JSON com mensagem sobre tempo em local inexistente
def test_weather_non_existent_place(client):
    response = client.post("/", json={"message": "Como está o tempo em Lalaland?"})
    assert response.status_code == 400
    data = response.get_json()
    assert data["response"] == 'Desculpe, não foi possível encontrar informações sobre o tempo em Lalaland'

# envia JSON vazio
def test_empty_json(client):
    response = client.post("/", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data["response"] == "Mensagem não fornecida"