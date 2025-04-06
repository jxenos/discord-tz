import requests
from bs4 import BeautifulSoup
import os
import logging

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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def check_terror_zone():
    try:
        response = requests.get('https://www.d2emu.com/tz')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        tz_tracker = soup.find(id='tz-tracker')
        if tz_tracker:
            next_zone_header = tz_tracker.find('h2', string='Next Terror Zone:')
            if next_zone_header:
                next_zone = next_zone_header.find_next_sibling('p').get_text(strip=True)
                if any(zone.lower() in next_zone.lower() for zone in TARGET_ZONES):
                    message = {"content": f'⚔️ **Upcoming Terror Zone:** {next_zone}!'}
                    requests.post(WEBHOOK_URL, json=message)
                    logger.info(f"Pinged zone: {next_zone}")
                else:
                    logger.info(f"No target zone match found for: {next_zone}")
    except Exception as e:
        logger.error(f"Error fetching or parsing the webpage: {e}")

if __name__ == "__main__":
    check_terror_zone()
