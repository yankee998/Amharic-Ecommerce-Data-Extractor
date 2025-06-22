from telethon.sync import TelegramClient
import pandas as pd
import os
import asyncio

# Telegram API credentials
api_id =  24319999 # Replace with your api_id (integer)
api_hash = '6e77649438c299ce7ea4b3be23bcc972'  # Replace with your api_hash (string)
phone = '+251941404384'  # Replace with your phone number (string)

# Read channels from Excel (no header)
channels_df = pd.read_excel('output/data/channels_to_crawl.xlsx', header=None)
channels = channels_df[0].head().tolist()[:5]  # Take first 5 channels from first column

async def scrape_channel(client, channel, limit=100):
    messages = []
    async for message in client.iter_messages(channel, limit=limit):
        try:
            data = {
                'channel': channel,
                'message_id': message.id,
                'date': message.date,
                'text': message.text,
                'views': message.views if message.views else 0,
                'sender_id': message.sender_id,
                'photo_path': None
            }
            if message.photo:
                photo_path = f'output/previews/{channel}_{message.id}.jpg'
                os.makedirs(os.path.dirname(photo_path), exist_ok=True)
                await message.download_media(file=photo_path)
                data['photo_path'] = photo_path
            messages.append(data)
        except Exception as e:
            print(f"Error processing message in {channel}: {e}")
            continue
    return messages

async def main():
    try:
        existing_data_path = 'output/processed/existing_telegram_data.csv'
        existing_df = pd.read_csv(existing_data_path, encoding='utf-8') if os.path.exists(existing_data_path) else pd.DataFrame()
        async with TelegramClient('session_name', api_id, api_hash) as client:
            all_messages = []
            for channel in channels:
                print(f"Scraping {channel}...")
                channel_messages = await scrape_channel(client, channel)
                all_messages.extend(channel_messages)
            new_df = pd.DataFrame(all_messages)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates(subset=['message_id', 'channel'])
            combined_df.to_csv('output/processed/raw_telegram_data.csv', index=False, encoding='utf-8')
            print("Combined data saved to output/processed/raw_telegram_data.csv")
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == '__main__':
    asyncio.run(main())