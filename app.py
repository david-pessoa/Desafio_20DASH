from flask import Flask, request, jsonify
from groq import Groq
from decouple import config

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():

    data = request.get_json()

    client = Groq(api_key=config("API_KEY"))
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
            "role": "system",
            "content": '''
            Você é um classificador de intenções.
            Sempre responda em JSON válido com este formato:
            {
                "clima": 0 ou 1  // 1 se a pergunta for sobre clima, 0 caso contrário
                "cidade": "nome da cidade" // se for pergunta sobre clima coloca o nome da cidade ou lugar falado, senão vazio"
                "resposta": "resposta" // Reescreva neste campo a sua resposta à mensagem do usuário
            }
            '''
            },
            {
                "role": "user",
                "content": data.message
            }
        ]
    )
    # Adiciona WeatherAPI
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

if __name__ == "__main__":
    app.run(debug=True)