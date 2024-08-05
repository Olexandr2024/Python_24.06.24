import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, JobQueue

# Ваш токен API Telegram
TELEGRAM_TOKEN = '7432658410:AAGMaxMTse86FebHjz-X6ttnI_7FJDGgJtQ'

# Начальная цена для отслеживания
target_price = None

# Функция для получения текущей цены ETH
def get_eth_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data['ethereum']['usd']

# Команда /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Используйте команду /setprice <цена>, чтобы установить целевую цену ETH.')

# Команда /setprice
async def set_price(update: Update, context: CallbackContext):
    global target_price
    try:
        target_price = float(context.args[0])
        await update.message.reply_text(f'Целевая цена ETH установлена на {target_price} USD.')
    except (IndexError, ValueError):
        await update.message.reply_text('Пожалуйста, введите корректную цену. Пример: /setprice 2500')

# Функция для проверки цены и отправки уведомления
async def check_price(context: CallbackContext):
    global target_price
    if target_price is not None:
        current_price = get_eth_price()
        if current_price >= target_price:
            await context.bot.send_message(chat_id=context.job.chat_id, text=f'Цена ETH достигла {current_price} USD!')
            target_price = None

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("setprice", set_price))

    # Настройка очереди заданий
    job_queue = application.job_queue
    job_queue.run_repeating(check_price, interval=60, first=0)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
