# Documentação da API
## Pré-requisitos
Para executar a API, é preciso ter Python 3.12 (ou mais recente) e instalar as seguintes dependências em suas versões mais atuais:

- flask
- groq
- decouple
- requests
- pytest (para execução de testes unitários)

### Instale elas com o comando abaixo
`pip install flask groq decouple requests`

### Crie um arquivo .env para salvar suas chaves de API
Crie um arquivo .env no diretório raíz desse projeto e salve suas chaves da API do modelo meta-llama/llama-4-scout-17b-16e-instruct e da WeatherAPI como representado abaixo:
```
LLM_API="chave da API do modelo meta-llama/llama-4-scout-17b-16e-instruct"
WEATHER_API='chave de API da WeatherAPI'
```

## Executando a API
Para executar a API, basta digitar o comando abaixo. A API será excutada de forma local, ouvindo na porta 8000
`python3 app.py`

Sendo assim, a rota para acessá-la é:
`http://127.0.0.1:8000` ou `http://localhost:8000`

## Estrutura
Para chamar a API, é preciso fazer uma requisição HTTP utilizando o método POST enviando um JSON com a seguinte estrutura:
```bash
POST
curl http://127.0.0.1:8000 -s \
	-H "Content-Type: application/json" \
	-d '{
	"message": "Aqui você escreve a mensagem que deseja enviar"
}'
```

Como resposta, a API responderá com outro arquivo JSON como mostrado abaixo:

```bash
200 OK {"response":"Olá, como posso ajudar você hoje?"}
```

## Mensagens sobre o tempo
Caso você esteja chamando a API para saber como está o tempo em determinado lugar, a API responderá com um JSON na mesma estrutura mostrada anteriormente, mas contendo a mensagem: "A previsão do tempo em São Paulo amanhã é de mínima 19 e máxima 25 graus.", caso a cidade seja São Paulo por exemplo.

```bash
POST
curl http://127.0.0.1:8000 -s \
	-H "Content-Type: application/json" \
	-d '{
	"message": "Qual é a previsão do tempo em São Paulo?"
}'
```

Como resposta, a API responderá com outro arquivo JSON como mostrado abaixo:

```bash
200 OK {"response":"A previsão do tempo em São Paulo amanhã é de mínima 19 e máxima 25 graus."}
```

## Erros
Se a estrutura para envio de mensagens não for seguida corretamente, a API está programada para retornar mensagens de erro.

### Erro na estrutura da mensagem
A API retorna "Mensagem de erro não fornecida" se não consegue obter a mensagem do usuário.  
Se o usuário manda um JSON vazio, por exemplo:
```bash
POST
curl http://127.0.0.1:8000 -s \
	-H "Content-Type: application/json" \
	-d '{}'
```
Resposta:
```bash
400 BAD REQUEST {"response":"Mensagem não fornecida"}
```

### Requisição para obter informações sobre o tempo de local inexistente
A API retorna "Desculpe, não foi possível encontrar informações sobre o tempo de Lalaland" se o usuário solicitar informações sobre o tempo de um local inexistente, como Lalaland, por exemplo.
```bash
POST
curl http://127.0.0.1:8000 -s \
	-H "Content-Type: application/json" \
	-d '{
	"message": "Como será o tempo amanhã em Lalaland?"
}'
```
Resposta:
```bash
400 BAD REQUEST {"response":"Desculpe, não foi possível encontrar informações sobre o tempo de Lalaland"}
```

### Erro interno
Caso ocorra um erro interno, a API responde com código de erro 500 com a mensagem sobre o respectivo erro.

## Testes Unitários
Comentar sobre os testes unitários realizados e o comando para executá-los