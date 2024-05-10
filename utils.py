import json
import requests

def load_conversations_from_json():
    with open('treinamento.json', 'r', encoding='utf-8') as file:
        conversations = json.load(file)
    return conversations

def train_chatbot_with_json(trainer):
    conversations = load_conversations_from_json()
    trainer.train(conversations)

def export_to_json(bot, filename):
    knowledge = []

    for statement in bot.storage.filter():
        knowledge.append({
            'text': statement.text
        })

    with open(filename, 'w') as json_file:
        json.dump(knowledge, json_file, indent=4)

def is_response_safe(response):
    prohibited_words = ["foda", "caralho", "porra"]

    for word in prohibited_words:
        if word in response.lower():
            return False
    return True

def safe_chatbot_response(bot, text):
    response = chatbot_response(bot, text)

    if is_response_safe(response):
        return response
    else:
        return "Desculpe, não posso fornecer essa informação."

def chatbot_response(bot, text):
    if text:
        response = bot.get_response(text)
        return response.text
    else:
        return "Desculpe, não entendi. Pode repetir, por favor?"

def get_weather(city):
    api_key = "533b29c37e8948be6c90ce13a97269d8"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    data = response.json()

    if response.status_code == 200:
        if "main" in data and "weather" in data:
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            return f"A temperatura em {city} é {temperature}°C com umidade {humidity}%."
        else:
            return "Não foi possível obter informações sobre o clima."
    else:
        return "Erro ao consultar a API de previsão do tempo."
