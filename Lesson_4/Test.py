import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш реальный токен Telegram бота
TOKEN = '7432658410:AAGMaxMTse86FebHjz-X6ttnI_7FJDGgJtQ'

# Переменная для хранения целевой цены, изначально None
TARGET_PRICE = None

# Функция для получения текущей цены Ethereum с использованием CoinGecko API
def get_ethereum_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data['ethereum']['usd']

# Функция для проверки цены и отправки уведомления, если цена достигла заданного значения
def check_ethereum_price(update: Update, context: CallbackContext):
    global TARGET_PRICE
    current_price = get_ethereum_price()
    if TARGET_PRICE is not None and current_price >= TARGET_PRICE:
        message = f"ETH price alert! Current price: ${current_price}"
        update.message.reply_text(message)
    else:
        update.message.reply_text(f"Текущая цена: ${current_price}")

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Добро пожаловать! Пожалуйста, введите цену, которую вы хотите отслеживать.")

# Функция для обработки текстового сообщения с введенной пользователем целевой ценой
def set_target_price(update: Update, context: CallbackContext):
    global TARGET_PRICE
    try:
        TARGET_PRICE = float(update.message.text)
        update.message.reply_text(f"Целевая цена установлена на ${TARGET_PRICE}.")
    except ValueError:
        update.message.reply_text("Некорректный ввод. Пожалуйста, введите корректное число.")

# Основная функция для создания и запуска бота
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики для различных команд и сообщений
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, set_target_price))
    dp.add_handler(CommandHandler("check", check_ethereum_price))

    # Запускаем бота
    updater.start_polling()
    print("Бот запущен и ожидает сообщений...")
    updater.idle()

if __name__ == '__main__':
    main()
