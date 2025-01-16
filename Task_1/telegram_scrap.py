from telethon import TelegramClient
import csv
import os
from dotenv import load_dotenv
import asyncio
# Load environment variables
load_dotenv('.env')

# Read credentials from the environment
api_id = os.getenv('TG_API_ID')
api_hash = os.getenv('TG_API_HASH')
phone = os.getenv('phone')
# Print to verify values (optional, for debugging)
print(f"API ID: {api_id}, API Hash: {api_hash}, Phone: {phone}")
# Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir):
    try:
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        async for message in client.iter_messages(entity, limit=10000):
            media_path = None
            if message.media and hasattr(message.media, 'photo'):
                filename = f"{channel_username}_{message.id}.jpg"
                media_path = os.path.join(media_dir, filename)
                try:
                    await client.download_media(message.media, media_path)
                except Exception as e:
                    print(f"Failed to download media for message {message.id}: {e}")
            
            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
    except Exception as e:
        print(f"Error scraping {channel_username}: {e}")
# Main function
async def main():
    # Initialize the client with a unique session name
    async with TelegramClient('new_v_session', api_id, api_hash, timeout=10) as client:
        await client.start()
        
        media_dir = 'photos'
        os.makedirs(media_dir, exist_ok=True)

        with open('telegram_data.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Channel Title', 'Channel Username', 'ID', 'Message', 'Date', 'Media Path'])
            
            channels = [
                '@Fashiontera',
                '@ZemenExpress',
                '@nevacomputer',
                '@meneshayeofficial',
                '@ethio_brand_collection',
            ]
            
            for channel in channels:
                print(f"Starting to scrape {channel}...")
                await scrape_channel(client, channel, writer, media_dir)
                print(f"Finished scraping data from {channel}")

# Run the main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())