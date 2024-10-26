import os
from binance.client import Client
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import mean_squared_error, mean_absolute_error
from datetime import datetime, timedelta

# Вставьте свои ключи API Binance
binance_api_key = 'ANdetxwbMPL0rGxzbabUauifMKkAt5CGv7Zrrs59R5U57VyGN2CzFRMIkXzDrxyv'
binance_api_secret = 'AmA14G2QiiMpjLdXM1SZ38TTYiwRshXUSziZUBnufVc5Jz20jSas6KTktAAUQD6p'

client = Client(binance_api_key, binance_api_secret)

# Загрузка исторических данных о цене ETH/USDT с шагом 1 час
try:
    candles = client.get_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_1HOUR)
except Exception as e:
    print(f"Ошибка при получении данных с Binance: {e}")
    exit(1)

# Преобразование данных в DataFrame
df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                     'close_time', 'quote_asset_volume', 'number_of_trades',
                                     'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
df['close'] = df['close'].astype(float)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

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

# Прогноз на 24 години вперед з кроком 1 година
def predict_next_hours(model, last_data, hours=24):
    predictions = []
    current_data = last_data[-60:]  # Використовуємо останні 60 годин для прогнозу
    current_data = current_data.reshape((1, current_data.shape[0], 1))  # Змінюємо форму масиву тут

    for _ in range(hours):
        predicted = model.predict(current_data)
        predictions.append(predicted[0, 0])
        # Додаємо новий прогноз до поточних даних
        current_data = np.append(current_data[:, 1:, :], predicted.reshape(1, 1, 1),
                                 axis=1)  # Змінюємо форму і напрямок додавання

    return scaler.inverse_transform(np.array(predictions).reshape(-1, 1))

# Отримуємо останні дані для прогнозу
last_data = scaled_data[-60:]
predicted_next_24_hours = predict_next_hours(model, last_data, hours=24)

# Виводимо прогнози
predicted_hours = [(datetime.now() + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M') for i in range(1, 25)]
predictions_output = pd.DataFrame({'Hour': predicted_hours, 'Predicted Price': predicted_next_24_hours.flatten()})

print("Прогнози на 24 години вперед:")
print(predictions_output)

# Збереження прогнозів на 24 години в CSV файл
predictions_output.to_csv('predictions_24_hours.csv', index=False)
print("Прогнози на 24 години збережені в 'predictions_24_hours.csv'.")
