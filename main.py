import discord
import requests
from bs4 import BeautifulSoup
import os
import logging
import asyncio

# Discord client setup
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
last_notified_zone = None

TARGET_ZONES = [
    'Catacombs',
    'Tal Rasha\'s Tomb',
    'Travincal',
    'Durance of Hate',
    'Chaos Sanctuary',
    'Worldstone Keep',
    'Forgotten Tower',
    'Arcane Sanctuary',
    'Halls of Vaught',
    'The Secret Cow Level'
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

async def check_terror_zone():
    global last_notified_zone
    client_channel = client.get_channel(CHANNEL_ID)

    try:
        response = requests.get('https://www.d2emu.com/tz')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tz_tracker = soup.find(id='tz-tracker')
        if tz_tracker:
            next_zone_header = tz_tracker.find('h2', string='Next Terror Zone:')
            if next_zone_header:
                next_zone = next_zone_header.find_next_sibling('p').get_text(strip=True)

                if any(zone.lower() in next_zone.lower() for zone in TARGET_ZONES) and next_zone != last_notified_zone:
                    await client_channel.send(f'⚔️ **Upcoming Terror Zone:** {next_zone}!')
                    logger.info(f"Pinged zone: {next_zone}")
                    last_notified_zone = next_zone
                else:
                    logger.info(f"No match found for: {next_zone}")

    except Exception as e:
        logger.error(f"Error fetching or parsing the webpage: {e}")

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user.name}')
    await check_terror_zone()
    await client.close()

client.run(DISCORD_TOKEN)
