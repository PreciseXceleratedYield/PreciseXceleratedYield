import telegram
import asyncio

import telegram
import asyncio

async def send_telegram_message(message_text, bot_token):
    bot = telegram.Bot(token='6409002088:AAH9mu0lfjvHl_IgRAgX7YrjJQa2Ew9qaLo')
    user_username = '6366694988'  # Replace with the appropriate username or ID
    await bot.send_message(chat_id=user_username, text=message_text)

# Run the asynchronous function
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    message_text = "Your message here"
    bot_token = 'YOUR_BOT_API_TOKEN'  # Replace with your actual bot token
    loop.run_until_complete(send_telegram_message(message_text, bot_token))





    




