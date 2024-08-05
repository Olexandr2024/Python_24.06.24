import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


TOKEN = '7432658410:AAGMaxMTse86FebHjz-X6ttnI_7FJDGgJtQ'


TARGET_PRICE = None


def get_ethereum_price():
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    return data['ethereum']['usd']


def check_ethereum_price(update: Update, context: CallbackContext):
    global TARGET_PRICE
    current_price = get_ethereum_price()
    if TARGET_PRICE is not None and current_price >= TARGET_PRICE:
        message = f"ETH price alert! Current price: ${current_price}"
        update.message.reply_text(message)
    else:
        update.message.reply_text(f"Текущая цена: ${current_price}")


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Добро пожаловать! Пожалуйста, введите цену, которую вы хотите отслеживать.")


def set_target_price(update: Update, context: CallbackContext):
    global TARGET_PRICE
    try:
        TARGET_PRICE = float(update.message.text)
        update.message.reply_text(f"Целевая цена установлена на ${TARGET_PRICE}.")
    except ValueError:
        update.message.reply_text("Некорректный ввод. Пожалуйста, введите корректное число.")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher


    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, set_target_price))
    dp.add_handler(CommandHandler("check", check_ethereum_price))


    updater.start_polling()
    print("Бот запущен и ожидает сообщений...")
    updater.idle()

if __name__ == '__main__':
    main()
