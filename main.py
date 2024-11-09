from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from fastapi import FastAPI
from datetime import datetime
import http.client

import os

app = FastAPI()
conn = http.client.HTTPSConnection(os.getenv('API_HOST'))

@app.get("/")
def root():
    return {"message": "This is the bot server running"}

def scrape_website(DEPARTURE, ARRIVAL):
    current_date = datetime.today().strftime('%Y-%m-%d')
    
    conn.request("GET", f"/flights/cheapest-one-way?fromEntityId={DEPARTURE}&toEntityId={ARRIVAL}&departDate={current_date}&currency=EUR", headers=headers)
    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))
    flights = response_data["data"]
    sorted_flights = sorted(flights, key=lambda x: x["price"])

    flight_strings = []
    for i in range(min(3, len(sorted_flights))):
        flight = sorted_flights[i]
        flight_string = f"Date: {flight['day']} | Price: ${flight['price']:.2f}"
        flight_strings.append(flight_string)

    return "\n".join(flight_strings)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome! Send me a command like /get CDG JFK to get the cheapest flights.")

async def get_flights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = ' '.join(context.args)  
    if len(context.args) < 2:
        await update.message.reply_text('Please provide both departure and arrival locations, like /get CDG JFK')
        return

    DEPARTURE, ARRIVAL = context.args[0], context.args[1]

    flight_details = scrape_website(DEPARTURE, ARRIVAL)

    await update.message.reply_text(f"Here are the top 3 cheapest flights:\n{flight_details}")

def run_bot():
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    get_handler = CommandHandler('get', get_flights)
    application.add_handler(get_handler)

    application.run_polling()

if __name__ == '__main__':
    import threading
    # Run the Telegram bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
