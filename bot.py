from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from utils import train_chatbot_with_json

def initial_training():
    bot = ChatBot(
        'Bot',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///database.sqlite3'
    )

    training_greetings = [
        "Hello",
        "Hi there!",
        "Hey",
        "Good morning",
        "Good afternoon",
        "Good evening"
    ]

    trainer_corpus = ChatterBotCorpusTrainer(bot)
    trainer_corpus.train('chatterbot.corpus.english')

    trainer = ListTrainer(bot)
    trainer.train(training_greetings)
    train_chatbot_with_json(trainer)

    return bot
