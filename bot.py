import discord
import os
from discord.ext import commands
import openai
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = ssl.get_default_verify_paths().openssl_cafile

# Discord bot token from environment variable
BOT_TOKEN = os.environ['BOT_TOKEN']

# OpenAI API key from environment variable
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Initializing the OpenAI API
openai.api_key = OPENAI_API_KEY

# Creating the Discord bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    # Ignoring messages from the bot itself
    if message.author == bot.user:
        return

    # Mentioning the bot to trigger a response
    if bot.user.mentioned_in(message):
        # Removing the bot mention from the message content
        content = message.content.replace(f'<@!{bot.user.id}>', '')

        # Sending the query to ChatGPT for a response
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=content,
            max_tokens=50,
            temperature=0.7,
            n=1,
            stop=None
        )

        # Sending the response back to the user
        await message.reply(response.choices[0].text.strip())

    await bot.process_commands(message)

bot.run(BOT_TOKEN)
