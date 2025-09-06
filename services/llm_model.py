from groq import Groq
from decouple import config

def get_llm_response(user_message):
# Realiza chamada para obter resposta do modelo de IA
    client = Groq(api_key=config("LLM_API"))
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
    return completion.choices[0].message.content.replace("`", '')