import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone = os.getenv('PHONE')

client = TelegramClient('session_name', api_id, api_hash)
channels = ['ZemenExpress', 'nevacomputer', 'meneshayeofficial', 'ethio_brand_collection', 'Leyueqa']

async def scrape_channel(channel, limit=100):
    data = []
    async for message in client.iter_messages(channel, limit=limit):
        msg_data = {
            'channel': channel,
            'message_id': message.id,
            'date': message.date,
            'sender': message.sender_id,
            'text': message.text,
            'views': message.views,
            'media': 'photo' if isinstance(message.media, MessageMediaPhoto) else 'none'
        }
        data.append(msg_data)
    return data

async def main():
    await client.start(phone=phone)
    all_data = []
    for channel in channels:
        print(f"Scraping {channel}...")
        channel_data = await scrape_channel(channel)
        all_data.extend(channel_data)
    df = pd.DataFrame(all_data)
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/telegram_data.csv', index=False, encoding='utf-8')
    print("Data saved to data/raw/telegram_data.csv")

if __name__ == '__main__':
    asyncio.run(main())