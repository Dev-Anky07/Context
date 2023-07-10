import os
import discord
from discord.ext import commands
import openai

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Discord client setup
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Set the environment variables
os.environ['BOT_TOKEN'] = 'MTEyNjYxNDk3NzkwNjc0OTU1MQ.Gl-klS.s2_CMv7bOS9cLfTWrwPjWBuPo2589smKd0cr9k'
os.environ['OPENAI_API_KEY'] = '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'

# OpenAI API setup
openai.api_key = os.environ["OPENAI_API_KEY"]

conversation_cache = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    conversation_id = message.channel.id
    conversation = conversation_cache.get(conversation_id)

    # Check if the message mentions the bot
    bot_mentioned = bot.user in message.mentions

    try:
        messages = [
            {'role': 'system', 'content': 'You are like a helpful friend who responds succinctly'}
        ]

        if conversation:
            messages.extend(conversation)

        messages.append({'role': 'user', 'content': message.content})

        if bot_mentioned:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=messages,
                temperature=0.1,  # Set the temperature parameter (adjust as desired)
                max_tokens=1000  # Set the maxTokens parameter (adjust as desired)
            )

            content = response['choices'][0]['message']['content']
            await message.reply(content)

        # Cache the conversation history
        conversation_cache[conversation_id] = messages

    except Exception as e:
        print(e)
        await message.reply("I'm sorry, I'm not smart enough to answer that.")

# Run the bot
bot.run(os.environ["BOT_TOKEN"])
