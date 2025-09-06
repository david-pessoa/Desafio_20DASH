from flask import Flask, request, jsonify
from services.llm_model import get_llm_response
from services.weather import get_weather
from werkzeug.exceptions import BadRequest
import json

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    try:
        try: # Verifica se o JSON enviado é válido
            data = request.get_json(force=True)
        except BadRequest:
            return jsonify({"response": "Mensagem inválida"}), 400

        # Pega a mensagem do usuário do corpo da requisição
        user_message = data.get("message") if data else None

        # Se não é possível obter a mensagem do usuário, envia resposta com erro
        if not user_message:
            return jsonify({"response": "Mensagem não fornecida"}), 400
        
        # Se a mensagem do usuário não for uma string, envia resposta com erro
        if not isinstance(user_message, str):
            return jsonify({"response": "Mensagem inválida"}), 400
        
        # Obtém resposta da IA e coloca num dicionário
        AI_response = get_llm_response(user_message)
        AI_dict = json.loads(AI_response)

        # Se o usuário perguntar sobre o clima, faz requisição para API da WeatherAPI
        if AI_dict["clima"]:
            CIDADE = AI_dict["cidade"]
            response = get_weather(CIDADE)
            
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
        return jsonify({"response": "Erro interno"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)