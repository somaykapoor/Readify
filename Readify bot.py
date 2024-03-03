import random
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '6502951788:AAENWpJ4iePPxRN-b_6CCP9GV8tlCUJe778'
BOT_USERNAME = '@img_scannerbot'

# Defining lists of possible links for each option
health_fitness_links = [
    "https://www.forbes.com/sites/bernardmarr/2023/01/04/5-important-health-and-fitness-tech-trends-for-2023/?sh=2db073722aaf",
    "https://www.forbes.com/sites/bernardmarr/2023/04/05/fit-for-the-future-10-trends-that-will-transform-the-fitness-industry/?sh=631230584000",
    "https://www.elle.com/uk/life-and-culture/culture/longform/a41063/fitness-trends-gym-classes-workout/",
    
]

entertainment_links = [
    "https://indianexpress.com/section/entertainment/",
    "https://www.thehindu.com/entertainment/",
    "https://hollywoodlife.com/",
    
]

marketing_business_links = [
    "https://www.livemint.com/industry/advertising",
    "https://brandequity.economictimes.indiatimes.com/news/marketing",
    "https://www.businesstoday.in/",
    
]

finance_links = [
    "https://www.moneycontrol.com/news/business/markets/",
    "https://www.financialexpress.com/",
    "https://www.cnbc.com/world/?region=world",
    
]

async def start_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.user_data['choice'] = None  # Reset the user's choice

    # Randomly choose a link for each option
    health_fitness_link = random.choice(health_fitness_links)
    entertainment_link = random.choice(entertainment_links)
    marketing_business_link = random.choice(marketing_business_links)
    finance_link = random.choice(finance_links)

    keyboard = [
        [InlineKeyboardButton("Health/Fitness", url=health_fitness_link)],
        [InlineKeyboardButton("Entertainment", url=entertainment_link)],
        [InlineKeyboardButton("Marketing/Business", url=marketing_business_link)],
        [InlineKeyboardButton("Finance", url=finance_link)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        'Hey! What do you want to read today?',
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text('How can I help you?')

def handle_response(text: str) -> str:
    processed = text.lower()

    if 'hello' in processed:
        return 'Hello, How can I help you?'
    
    if 'hi' in processed:
        return 'Hi there'
    
    if 'hey' in processed:
        return 'Hey there'
    
    if 'kiddan' in processed:
        return 'vdia, tuhi sunao'
    
    if 'How to access articles' in processed:
        return 'join this Telegram Channel: t.me/img_scan'
    

    return 'I do not understand, Please try again!'

async def handle_message(update: Update, context: CallbackContext):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting the bot')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
