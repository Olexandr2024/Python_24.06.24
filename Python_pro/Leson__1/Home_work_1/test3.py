import os
from binance.client import Client
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Conv1D, Flatten, Input
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from textblob import TextBlob
from arch import arch_model
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
import nltk
import torch

if torch.cuda.is_available():
    print("GPU доступен!")
    print(f"Используемая версия CUDA: {torch.version.cuda}")
else:
    print("GPU недоступен.")

nltk.download('vader_lexicon')

# Вставьте свои ключи API Binance и NewsAPI
binance_api_key = 'ANdetxwbMPL0rGxzbabUauifMKkAt5CGv7Zrrs59R5U57VyGN2CzFRMIkXzDrxyv'
binance_api_secret = 'AmA14G2QiiMpjLdXM1SZ38TTYiwRshXUSziZUBnufVc5Jz20jSas6KTktAAUQD6p'
newsapi_key = '9b72d08add6743679e1114b1b57e0122'

client = Client(binance_api_key, binance_api_secret)

# Загрузка исторических данных о цене ETH/USDT
try:
    candles = client.get_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_1DAY)
except Exception as e:
    print(f"Ошибка при получении данных с Binance: {e}")
    exit(1)

# Преобразование данных в DataFrame
df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                     'close_time', 'quote_asset_volume', 'number_of_trades',
                                     'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

df['close'] = df['close'].astype(float)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Вирахування CRT (Candle Range Trading) та зростання
df['CRT'] = df['high'].astype(float) - df['low'].astype(float)
df['CRT_growth'] = df['CRT'].pct_change()
df['price_growth'] = df['close'].pct_change()


# Кореляція між зростанням CRT та ціни
crt_price_corr = df[['CRT_growth', 'price_growth']].corr().iloc[0, 1]
print(f"Кореляція між ростом CRT і ціною: {crt_price_corr}")

# Нормалізація даних для LSTM моделі
data = df['close'].values.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Підготовка вибірок для навчання і тестування
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size - 60:]

# Функція для створення вибірки для LSTM
def create_dataset(dataset, look_back=60):
    x, y = [], []
    for i in range(look_back, len(dataset)):
        x.append(dataset[i - look_back:i, 0])
        y.append(dataset[i, 0])
    return np.array(x), np.array(y)

x_train, y_train = create_dataset(train_data)
x_test, y_test = create_dataset(test_data)

x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Параметри LSTM моделі
num_neurons = 100
num_layers = 2
dropout_rate = 0.2

# Побудова LSTM моделі
model = Sequential()
for i in range(num_layers):
    model.add(LSTM(num_neurons, return_sequences=(i < num_layers - 1), input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(dropout_rate))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Обучение модели
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model.fit(x_train, y_train, epochs=100, batch_size=16, validation_split=0.2, callbacks=[early_stopping], verbose=1)

# Прогнозирование цен
predicted_price_lstm = model.predict(x_test)
predicted_price_lstm = scaler.inverse_transform(predicted_price_lstm)

# Оценка LSTM модели
mse_lstm = mean_squared_error(y_test, predicted_price_lstm)
mae_lstm = mean_absolute_error(y_test, predicted_price_lstm)
print(f'MSE LSTM: {mse_lstm}')
print(f'MAE LSTM: {mae_lstm}')

# Сентимент-аналіз новин
current_date = datetime.now()
start_date = current_date - timedelta(days=30)
start_date_str = start_date.strftime('%Y-%m-%d')
current_date_str = current_date.strftime('%Y-%m-%d')

# Підключення до NewsAPI
newsapi = NewsApiClient(api_key=newsapi_key)
all_articles = newsapi.get_everything(
    q='Ethereum',
    from_param=start_date_str,
    to=current_date_str,
    language='en',
    sort_by='relevancy'
)

print(f"Дата начала: {start_date_str}, дата конца: {current_date_str}")
print(f"Количество статей: {len(all_articles['articles'])}")

# Сентимент-аналіз функція
def sentiment_analysis(articles):
    sentiments = []
    for article in articles['articles']:
        description = article.get('description')
        if description:
            analysis = TextBlob(description)
            sentiments.append(analysis.sentiment.polarity)
    return np.mean(sentiments)

average_sentiment = sentiment_analysis(all_articles)
print(f"Средний сентимент новостей: {average_sentiment}")

# Регресійні моделі
# Лінійна регресія
linear_model = LinearRegression()
X = np.array(range(len(df))).reshape(-1, 1)
y = df['close'].values
linear_model.fit(X, y)
linear_predictions = linear_model.predict(X)

# Поліноміальна регресія
poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(X)
poly_model = LinearRegression()
poly_model.fit(X_poly, y)
poly_predictions = poly_model.predict(X_poly)

# Random Forest
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X, y)
predicted_price_rf = rf_model.predict(X)

# XGBoost
xgb_model = XGBRegressor()
xgb_model.fit(X, y)
xgb_predictions = xgb_model.predict(X)

# CNN модель
cnn_model = Sequential()
cnn_model.add(Input(shape=(x_train.shape[1], 1)))
cnn_model.add(Conv1D(filters=32, kernel_size=2, activation='relu'))
cnn_model.add(Flatten())
cnn_model.add(Dense(1))
cnn_model.compile(optimizer='adam', loss='mean_squared_error')

cnn_model.fit(x_train, y_train, epochs=100, batch_size=16, validation_split=0.2, callbacks=[early_stopping], verbose=1)
predicted_price_cnn = cnn_model.predict(x_test)
predicted_price_cnn = scaler.inverse_transform(predicted_price_cnn)

mse_cnn = mean_squared_error(y_test, predicted_price_cnn)
mae_cnn = mean_absolute_error(y_test, predicted_price_cnn)
print(f'MSE CNN: {mse_cnn}')
print(f'MAE CNN: {mae_cnn}')

# GARCH модель
scaled_returns = df['close'].pct_change().dropna() * 100  # Відмасштабування на 100
garch_model = arch_model(scaled_returns, vol='Garch', p=1, q=1)
garch_fit = garch_model.fit(disp='off')
print(garch_fit.summary())

# Зберігаємо прогнози від різних моделей
preds_lstm = predicted_price_lstm.flatten()
preds_cnn = predicted_price_cnn.flatten()
preds_rf = predicted_price_rf
preds_xgb = xgb_predictions
preds_lr = linear_predictions

# Проверка размеров
print(f"y_test size: {len(y_test)}")
print(f"preds_lstm size: {len(preds_lstm)}")
print(f"preds_cnn size: {len(preds_cnn)}")
print(f"preds_rf size: {len(preds_rf)}")
print(f"preds_xgb size: {len(preds_xgb)}")
print(f"preds_lr size: {len(preds_lr)}")

# Вирахуйте MAE (або інший показник помилки) для порівняння
mae_lstm = mean_absolute_error(y_test, preds_lstm)
mae_cnn = mean_absolute_error(y_test, preds_cnn)
mae_rf = mean_absolute_error(y_test, preds_rf[:len(y_test)])  # Обеспечим, чтобы размеры совпадали
mae_xgb = mean_absolute_error(y_test, preds_xgb[:len(y_test)])  # Обеспечим, чтобы размеры совпадали
mae_lr = mean_absolute_error(y_test, preds_lr[:len(y_test)])  # Обеспечим, чтобы размеры совпадали

print(f'MAE LSTM: {mae_lstm}')
print(f'MAE CNN: {mae_cnn}')
print(f'MAE Random Forest: {mae_rf}')
print(f'MAE XGBoost: {mae_xgb}')
print(f'MAE Linear Regression: {mae_lr}')

# Об'єднання прогнозів в один DataFrame для подальшого аналізу
predictions_df = pd.DataFrame({
    'True Price': scaler.inverse_transform(y_test.reshape(-1, 1)).flatten(),
    'LSTM': preds_lstm,
    'CNN': preds_cnn,
    'Random Forest': preds_rf[:len(y_test)],
    'XGBoost': preds_xgb[:len(y_test)],
    'Linear Regression': preds_lr[:len(y_test)]
})


# Прогноз на 7 днів вперед
def predict_next_hours(model, last_data, hours=24):
    predictions = []
    current_data = last_data[-60:]  # Використовуємо останні 60 значень для прогнозу
    current_data = current_data.reshape((1, current_data.shape[0], 1))

    for _ in range(hours):
        predicted = model.predict(current_data)
        predictions.append(predicted[0, 0])
        # Додаємо новий прогноз до поточних даних
        current_data = np.append(current_data[:, 1:, :], predicted.reshape(1, 1, 1), axis=1)  # Оновлюємо поточні дані

    return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))


# Отримуємо останні дані для прогнозу
last_data = scaled_data[-60:]



# Прогнозуємо ціни на 7 днів вперед
predicted_next_hours = predict_next_hours(model, last_data, hours=24)

# Виводимо прогнози
predicted_times = [(datetime.now() + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M') for i in range(1, 25)]
hourly_predictions_output = pd.DataFrame({'Time': predicted_times, 'Predicted Price': predicted_next_hours.flatten()})

print("Прогнози на 24 години вперед:")
print(hourly_predictions_output)

# Збереження прогнозів на 24 години в CSV файл
hourly_predictions_output.to_csv('predictions_24_hours.csv', index=False)
print("Прогнози на 24 години збережені в 'predictions_24_hours.csv'.")