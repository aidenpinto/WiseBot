import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()

# Loads in your Discord Bot token from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Loads in your OpenAI API Key from the .env file

openai.api_key = os.getenv('OPENAI_API_KEY')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

# When the bot connects successfully, prints out a message to say that it has connected.
@client.event
async def on_ready():
    print('We have successfully logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
   
   # Makes the bot only respond to messages from user, not from itself
    if message.author == client.user:
        return

    # Checks if the bot was mentioned in the message (using @)
    if client.user in message.mentions:

        # Uses GPT-3.5 Turbo to generate a response to the message
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # Define the bot's personality in the line below
                {"role": "system", "content": "You are a helpful assistant."},   
                {"role": "user", "content": message.content}
            ]
        )
        # Sends the response as a message from the bot
        await message.channel.send(response.choices[0].message.content)

# Starts the bot
client.run(TOKEN)