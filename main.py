import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()

# Loads in your Discord Bot Token and sets it as a constant. This used to connect the bot to Discord's API.
TOKEN = os.getenv('DISCORD_TOKEN')

# Loads in your OpenAI API key and sets it as a variable.
openai.api_key = os.getenv('OPENAI_KEY')

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

# When the bot connects successfully to the Discord API, this prints out a message to say that it has connected.

@client.event
async def on_ready():
    print('Successfully connected as {0.user}'.format(client))

@client.event
async def on_message(message):

    # Makes the bot only respond to messages from the user/question asker, not from itself.

    if message.author == client.user:
        return

    # Checks if the bot was mentioned in the message (using @)

    if client.user in message.mentions:

        # This uses the OpenAI API to generate a response to the question

        async with message.channel.typing():

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    # Customizes the personality of the assistant. Change the quotes after "content" to edit the personality.
                    {"role": "system", "content": "You are a helpful assistant."},   
                    {"role": "user", "content": message.content}
            ]
        )
        
        # Sends the response as a message from the bot.

        await message.channel.send(response.choices[0].message.content)

# This line runs the bot.
client.run(TOKEN)