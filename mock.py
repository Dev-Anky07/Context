import os
import discord
from dotenv import load_dotenv
import openai

load_dotenv()
token = os.getenv('BOT_TOKEN')
openai_key = os.getenv('OPENAI_API_KEY')

#connect to openai
openai.api_key = openai_key

intents = discord.Intents.all()
client = discord.Client(command_prefix = '!', intents = intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#test sending a message and receiving a message from a bot
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #check if the bot is mentioned in the message
    if client.user.mentioned_in(message):
        response = openai.Completion.create(
            engine = 'gpt-4',
            prompt = f'{message.content}',
            temperature = 0.5 ,
            max_tokens = 2048,
        )
    await message.channel.send(response.choices[0].text)

client.run(token)