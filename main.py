import requests
from bs4 import BeautifulSoup
import os
import logging
import sys

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

def check_terror_zone():
    try:
        response = requests.get('https://www.d2emu.com/tz')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        current_zone = soup.find(id='a2x')
        next_zone = soup.find(id='x2a')

        if current_zone:
            current_zone_text = current_zone.get_text(strip=True)
            logger.info(f"Current Terror Zone: {current_zone_text}")
            sys.stdout.flush()
        
        if next_zone:
            next_zone_text = next_zone.get_text(strip=True)
            logger.info(f"Next Terror Zone: {next_zone_text}")
            sys.stdout.flush()
            
            if any(zone.lower() in next_zone_text.lower() for zone in TARGET_ZONES):
                message = {"content": f'⚔️ **Upcoming Terror Zone:** {next_zone_text}!'}
                requests.post(WEBHOOK_URL, json=message)
                logger.info(f"Pinged zone: {next_zone_text}")
                sys.stdout.flush()
            else:
                logger.info(f"No target zone match found for: {next_zone_text}")
                sys.stdout.flush()

    except Exception as e:
        logger.error(f"Error fetching or parsing the webpage: {e}")
        sys.stdout.flush()

if __name__ == "__main__":
    check_terror_zone()
