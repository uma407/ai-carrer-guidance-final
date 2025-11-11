import os
from career_chatbot import CareerChatbot

print("ENV OPENAI_API_KEY set:", bool(os.environ.get("OPENAI_API_KEY")))
bot = CareerChatbot()
client = getattr(bot, 'client', None)
print("CareerChatbot.client present:", bool(client))
print("CareerChatbot.client.api_key:", getattr(client, 'api_key', None))
