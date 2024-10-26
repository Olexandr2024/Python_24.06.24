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
from arch import arch_model  # Імпорт GARCH
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import warnings

# Загрузка ресурса vader_lexicon для SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# Вставьте свои ключи API Binance и NewsAPI
binance_api_key = 'ANdetxwbMPL0rGxzbabUauifMKkAt5CGv7Zrrs59R5U57VyGN2CzFRMIkXzDrxyv'
binance_api_secret = 'AmA14G2QiiMpjLdXM1SZ38TTYiwRshXUSziZUBnufVc5Jz20jSas6KTktAAUQD6p'
newsapi_key = '9b72d08add6743679e1114b1b57e0122'

# Подключение к API Binance
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

# Используем цены закрытия для анализа
data = df['close'].values.reshape(-1, 1)

# Нормализация данных
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Подготовка обучающей и тестовой выборок
train_size = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_size]
test_data = scaled_data[train_size - 60:]

# Функция для создания обучающих данных для LSTM
def create_dataset(dataset, look_back=100):
    x, y = [], []
    for i in range(look_back, len(dataset)):
        x.append(dataset[i - look_back:i, 0])
        y.append(dataset[i, 0])
    return np.array(x), np.array(y)

x_train, y_train = create_dataset(train_data)
x_test, y_test = create_dataset(test_data)

# Преобразование данных для подачи в LSTM
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Параметры модели
num_neurons = 500
num_layers = 3
dropout_rate = 0.2

# Строим модель LSTM
model = Sequential()
for i in range(num_layers):
    model.add(LSTM(num_neurons, return_sequences=(i < num_layers - 1), input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(dropout_rate))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Обучение модели
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
model.fit(x_train, y_train, epochs=25, batch_size=16, validation_split=0.2, callbacks=[early_stopping], verbose=1)

# Прогнозирование цен
predicted_price = model.predict(x_test)
predicted_price = scaler.inverse_transform(predicted_price)

# Оценка модели по метрикам
mse = mean_squared_error(y_test, predicted_price)
mae = mean_absolute_error(y_test, predicted_price)
print(f'MSE: {mse}')
print(f'MAE: {mae}')

# Получение текущей даты
current_date = datetime.now()

# Вычисляем дату 30 дней назад
start_date = current_date - timedelta(days=30)

# Преобразуем даты в формат, подходящий для запроса (например, 'YYYY-MM-DD')
start_date_str = start_date.strftime('%Y-%m-%d')
current_date_str = current_date.strftime('%Y-%m-%d')

# Подключение к NewsAPI для поиска новостей по Bitcoin
newsapi = NewsApiClient(api_key=newsapi_key)
all_articles = newsapi.get_everything(
    q='Bitcoin',
    from_param=start_date_str,  # Дата 30 дней назад
    to=current_date_str,  # Текущая дата
    language='en',
    sort_by='relevancy'
)
print(f"Начальная дата: {start_date_str}, Конечная дата: {current_date_str}")

print(f"Количество найденных статей: {len(all_articles['articles'])}")
for article in all_articles['articles'][:5]:
    description = article.get('description')
    if description:
        analysis = TextBlob(description)
        print(f"Описание: {description}\nСентимент: {analysis.sentiment.polarity}")
    else:
        print("Нет описания.")

# Функция для сентимент-аналитики
def sentiment_analysis(df, articles):
    sentiments = []
    timestamps = []

    for article in articles['articles']:
        description = article.get('description')
        published_at = article.get('publishedAt')
        if description and published_at:
            analysis = TextBlob(description)
            polarity = analysis.sentiment.polarity
            sentiments.append(polarity)
            timestamps.append(pd.to_datetime(published_at))

    # Создание DataFrame для сентимент-анализа
    sentiment_df = pd.DataFrame({'timestamp': timestamps, 'sentiment': sentiments})

    # Проверяем, если timestamps имеют временную зону и удаляем ее
    if sentiment_df['timestamp'].dt.tz is not None:
        sentiment_df['timestamp'] = sentiment_df['timestamp'].dt.tz_localize(None)

    # Группировка по времени и усреднение сентимента
    sentiment_df = sentiment_df.groupby('timestamp').mean().reset_index()

    # Убедимся, что 'timestamp' в df тоже без временной зоны
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)

    # Фильтрация DataFrame по дате
    df_filtered = df[df['timestamp'] >= start_date]  # оставляем только последние 30 дней

    # Объединение с учетом временного диапазона
    df_filtered = pd.merge(df_filtered, sentiment_df, on='timestamp', how='left')
    df_filtered['sentiment'].fillna(0, inplace=True)

    return df_filtered

# Применение сентимент-аналитики к DataFrame
df_sentiment = sentiment_analysis(df, all_articles)

# Вывод результатов
print(df_sentiment.head())

# Регрессия
# Линейная регрессия
linear_model = LinearRegression()
X = np.array(range(len(df_sentiment))).reshape(-1, 1)
y = df_sentiment['close'].values
linear_model.fit(X, y)
linear_predictions = linear_model.predict(X)

# Полиномиальная регрессия
poly_features = PolynomialFeatures(degree=2)
X_poly = poly_features.fit_transform(X)
poly_model = LinearRegression()
poly_model.fit(X_poly, y)
poly_predictions = poly_model.predict(X_poly)

# Модель Random Forest
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X, y)
rf_predictions = rf_model.predict(X)

# Модель XGBoost
xgb_model = XGBRegressor()
xgb_model.fit(X, y)
xgb_predictions = xgb_model.predict(X)

# Нейронная сеть CNN
cnn_model = Sequential()
cnn_model.add(Input(shape=(100, 1)))  # Измените на правильную форму, соответствующую вашим данным
cnn_model.add(Conv1D(filters=64, kernel_size=2, activation='relu'))
cnn_model.add(Dropout(0.2))
cnn_model.add(Flatten())
cnn_model.add(Dense(1))
cnn_model.compile(optimizer='adam', loss='mean_squared_error')

# Обучение модели CNN
cnn_model.fit(x_train, y_train, epochs=15, batch_size=16, validation_split=0.2, callbacks=[early_stopping], verbose=1)

# Прогнозирование цен с помощью CNN
cnn_predictions = cnn_model.predict(x_test)

# GARCH модель для прогнозирования волатильности
returns = df['close'].pct_change().dropna()  # Получаем процентные изменения
scaled_returns = returns * 100  # Масштабируем данные
model_garch = arch_model(scaled_returns, vol='Garch', p=1, q=1, rescale=False)  # Создаем GARCH модель
model_garch_fit = model_garch.fit(disp='off')  # Обучаем модель
print(model_garch_fit.summary())  # Выводим результаты

last_date = df['timestamp'].iloc[-1]
predicted_dates = [last_date + timedelta(days=i) for i in range(1, len(predicted_price) + 1)]
# Вывод прогнозов
for i in range(len(predicted_dates)):
    print(f"Прогнозируемая цена на {predicted_dates[i].strftime('%Y-%m-%d')}: {predicted_price[i][0]:.2f}")
