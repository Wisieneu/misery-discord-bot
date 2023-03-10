import discord
from discord import app_commands
import responses
import random

async def send_message(message, user_message):
    try:
        response = responses.get_response(message)
        if response:
            await message.channel.send(response)
        else: 
            return
    except Exception as e:
        print(e)


def run_discord_bot(TOKEN):
    
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        synced = await tree.sync()
        print(f'{len(synced)} commands have been synced successfully.')
        print('{} has been turned on successfully.\n'.format(client.user))
    
    # Logging every message the bot is able to see (if not sent by the bot itself)
    @client.event
    async def on_message(message):
        if message.author != client.user:
            if message.guild.name:
                message_log = f'{str(message.guild.name)} ==> #{str(message.channel)}\n'
            else: 
                message_log = '## DIRECT MESSAGE ##\n'
            message_log += f'{str(message.author)}: "{str(message.content)}"\n'
            if message.attachments:
                message_log += str(message.attachments)
            print(message_log)
            await send_message(message, str(message.content))

    @tree.command(name = "roll", description = "Rolls a random number between 1 and input integer") #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
    async def first_command(interaction, input_int: int):
        await interaction.response.send_message(f'Rolled: {random.randint(1, input_int)}')

    client.run(TOKEN)