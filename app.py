from flask import Flask, request, jsonify
from groq import Groq
from decouple import config
import requests
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    try:
        # Pega a mensagem do usuário do corpo da requisição
        user_message = request.get_json().get("message")

        # Se não é possível obter a mensagem do usuário, envia resposta com erro
        if not user_message:
            return jsonify({"response": "Mensagem não fornecida"}), 400

        # Realiza chamada para obter resposta do modelo de IA
        client = Groq(api_key=config("API_KEY"))
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                "role": "system",
                "content": '''
                Você é um classificador de intenções.
                OBS: Não envolva sua resposta com acento grave ou qualquer outro tipo de caractere
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
                    "content": user_message
                }
            ]
        )
        
        # Coloca resposta da IA num dicionário
        AI_response = completion.choices[0].message.content.replace("`", '')
        AI_dict = json.loads(AI_response)

        # Se o usuário perguntar sobre o clima, faz requisição para API da WeatherAPI
        if AI_dict["clima"]:
            DIAS = 2
            CIDADE = AI_dict["cidade"]
            URL = f'http://api.weatherapi.com/v1/forecast.json?key={config('WEATHER_API')}&q={CIDADE}&days={DIAS}&aqi=no&alerts=no&lang=pt'
            response = requests.get(URL)

            if response.status_code == 400:
                return jsonify({'response': f'Desculpe, não foi possível encontrar informações sobre o tempo em {CIDADE}'}), 400

            dados = response.json()
            previsao = dados['forecast']['forecastday'][1] #Previsão do tempo para amanhã
            max_temp = round(previsao["day"]["maxtemp_c"])
            min_temp = round(previsao["day"]["mintemp_c"])

            return jsonify({"response": f"A previsão do tempo em {AI_dict['cidade']} amanhã é de mínima {min_temp} e máxima {max_temp} graus."})

        # Se a pergunta for sobre qualquer outro assunto, apenas envia a resposta da IA
        else:
            return jsonify({"response": AI_dict["resposta"]})
        
        # Se acontece algum erro no processo, envia mensagem do erro
    except Exception as e:
        return jsonify({"response": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)