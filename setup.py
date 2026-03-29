# setup.py
import discord
from discord.ext import commands
import asyncio
import os
import random
from datetime import datetime

# Get tokens and channel ID from environment variables
TOKENS = os.getenv('TOKENS')
CHANNEL_ID = os.getenv('CHANNEL_ID')

# Validate environment variables
if not TOKENS:
    print("ERROR: TOKENS environment variable not set!")
    print("Please set TOKENS as a comma-separated list (e.g., token1,token2,token3)")
    exit(1)

if not CHANNEL_ID:
    print("ERROR: CHANNEL_ID environment variable not set!")
    print("Please set CHANNEL_ID in your Render environment variables")
    exit(1)

# Parse tokens (comma-separated)
token_list = [token.strip() for token in TOKENS.split(',')]
print(f"Loaded {len(token_list)} tokens")

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    print(f"ERROR: CHANNEL_ID must be a number! Got: {CHANNEL_ID}")
    exit(1)

# Create bot instances
bots = []
for i, token in enumerate(token_list):
    bot = commands.Bot(command_prefix=f"!{i}", intents=discord.Intents.default())
    bots.append(bot)

async def send_message_to_channel(bot, channel_id, message):
    """Send a message to a specific channel"""
    try:
        channel = bot.get_channel(channel_id)
        if not channel:
            channel = await bot.fetch_channel(channel_id)
        
        await channel.send(message)
        print(f"[{datetime.now()}] Sent message from bot: {message[:50]}...")
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Error sending message: {e}")
        return False

async def rotate_messages():
    """Continuously send messages from different bots"""
    messages = [
        "Hello from bot!",
        "Another message!",
        "This is a test",
        "Random message here",
        "Discord bot activity",
        "How's everyone doing?",
        "Just saying hi!",
        "Bot is active",
        "Sending from different tokens",
        "Message rotation active"
    ]
    
    message_index = 0
    bot_index = 0
    
    while True:
        # Rotate through bots
        current_bot = bots[bot_index % len(bots)]
        current_message = messages[message_index % len(messages)]
        
        # Add random number to message to make it unique
        final_message = f"{current_message} [{random.randint(1000, 9999)}]"
        
        await send_message_to_channel(current_bot, CHANNEL_ID, final_message)
        
        # Update indices
        bot_index += 1
        message_index += 1
        
        # Wait random time between 30-60 seconds
        await asyncio.sleep(random.randint(30, 60))

@bots[0].event
async def on_ready():
    print(f"Bot 1 is ready as {bots[0].user}")
    # Start the message rotation for all bots
    asyncio.create_task(rotate_messages())

# Setup event handlers for other bots
for i, bot in enumerate(bots[1:], start=2):
    @bot.event
    async def on_ready(b=bot, num=i):
        print(f"Bot {num} is ready as {b.user}")

# Run all bots
async def main():
    # Start all bots
    tasks = []
    for i, bot in enumerate(bots):
        token = token_list[i]
        task = asyncio.create_task(bot.start(token))
        tasks.append(task)
    
    # Wait for all bots to finish (they won't unless error)
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    print("Starting Discord bot with multiple tokens...")
    print(f"Target channel ID: {CHANNEL_ID}")
    print(f"Number of bots: {len(token_list)}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")
