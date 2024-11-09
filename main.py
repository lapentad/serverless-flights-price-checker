import httpx
import asyncio
from fastapi import FastAPI
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging
import uvicorn
from uvicorn import Config, Server

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

headers = {
    'x-rapidapi-key': "40f496afedmsh78eba06b6b50a1ap123d38jsna3865a02a679",
    'x-rapidapi-host': "sky-scanner3.p.rapidapi.com"
}

# FastAPI Setup
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the bot server running"}

@app.get("/start")
async def start_bot():
    # Start the Telegram bot in the background
    asyncio.create_task(run_telegram_bot())
    return {"message": "Telegram bot has been started!"}

# Async function to scrape flight data
async def scrape_website(DEPARTURE, ARRIVAL):
    current_date = datetime.today().strftime('%Y-%m-%d')
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://sky-scanner3.p.rapidapi.com/flights/cheapest-one-way",
            params={
                'fromEntityId': DEPARTURE,
                'toEntityId': ARRIVAL,
                'departDate': current_date,
                'currency': 'EUR'
            },
            headers=headers
        )
        response_data = response.json()
        flights = response_data.get("data", [])
        sorted_flights = sorted(flights, key=lambda x: x["price"])

        flight_strings = []
        for i in range(min(3, len(sorted_flights))):
            flight = sorted_flights[i]
            flight_string = f"Date: {flight['day']} | Price: €{flight['price']:.2f}"
            flight_strings.append(flight_string)

        return "\n".join(flight_strings)

# Telegram Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Send me a command like /get CDG JFK to get the cheapest flights.")

async def get_flights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text('Please provide both departure and arrival locations, like /get CDG JFK')
        return

    DEPARTURE, ARRIVAL = context.args[0], context.args[1]
    flight_details = await scrape_website(DEPARTURE, ARRIVAL)
    await update.message.reply_text(f"Here are the top 3 cheapest flights:\n{flight_details}")

# Run the Telegram bot asynchronously
async def run_telegram_bot():
    application = ApplicationBuilder().token("7591640556:AAH5u6w5Y7-QRvdRn5b_eJ8KH6CNwxv5pLM").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('get', get_flights))
    await application.initialize()
    await application.start()
    await application.updater.start_polling()

async def main():
    # Create a Uvicorn Config and Server manually to avoid using asyncio.run()
    config = Config(app=app, host="0.0.0.0", port=8080)
    server = Server(config=config)

    # Start FastAPI server and Telegram bot in the same event loop
    server_task = asyncio.create_task(server.serve())  # This runs uvicorn's event loop

    # Wait for the server task to complete
    await server_task

if __name__ == "__main__":
    # Run the application in the asyncio event loop
    asyncio.run(main())
