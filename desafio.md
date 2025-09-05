# Desafio técnico estágio 20DASH
Criar uma API de Chatbot que retorne a previsao do tempo para uma cidade, caso o usuario estiver perguntando algo sobre o assunto. Caso contrário o bot deve conversar normalmente com o usuario.

Exemplos de requests que a API deve receber e responder:

POST
```bash
curl http://127.0.0.1:8000 -s \
	-H "Content-Type: application/json" \
	-d '{
	"message": "Qual era a principal guitarra do Jimi Hendrix?"
}'

```
resposta
```bash
200 OK {"response":"A principal guitarra do Jimi Hendrix era a Fender Stratocaster."}}
```

POST
```bash
curl http://127.0.0.1:8000 -s \
	-H "Content-Type: application/json" \
	-d '{
	"message": "aeee chove amanha em Bertioga sera?"
}'
```
resposta
```bash
200 OK {"response":"A previsão do tempo em Bertioga amanha é de mínima 20 e máxima 24 graus."}}
```

Requisitos:
* Para a LLM utilizar o groq.com com o modelo meta-llama/llama-4-scout-17b-16e-instruct (possui acesso grátis a API KEY)
* Criar pelo menos 2 testes unitarios. Sendo que um deve falar sobre previsão de tempo, e outro não.
* Incluir documentação sobre como executar a API (instalação de dependencias, execução etc) e também das rotas de acesso e respostas esperadas (requests e responses)
* Subir o projeto final em uma conta qualquer do Github e enviar o link final.


Observações:
* A linguagem ou framework usado para API  pode ser qualquer uma a escolha, porém sempre damos preferência para Chalice/Python ou Node.js pela escalabilidade.
* Para a consulta da previsão do tempo fica a cargo do candidato escolher qual usar.