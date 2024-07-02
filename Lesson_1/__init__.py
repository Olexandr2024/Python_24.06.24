import pandas as pd
import os
from prophet import Prophet
import matplotlib.pyplot as plt

# Укажите полный путь к файлу
file_path = 'D:\Учеба ИТ\Python_24.06.24\Lesson_1/book_sales.xlsx'

# Проверка наличия файла и прав доступа
if not os.path.exists(file_path):
    print(f"Файл не найден: {file_path}")
elif not os.access(file_path, os.R_OK):
    print(f"Нет прав для чтения файла: {file_path}")
else:
    try:
        # Чтение данных из Excel
        df = pd.read_excel(file_path, sheet_name='Sales')

        # Переименуем колонки для Prophet
        df = df.rename(columns={'date': 'ds', 'sales': 'y'})

        # Задаем данные о праздниках
        holidays = pd.DataFrame({
            'holiday': 'holiday',
            'ds': pd.to_datetime(['2023-12-25', '2024-01-01', '2024-04-01']),  # Пример праздников
            'lower_window': 0,
            'upper_window': 1,
        })

        # Создаем модель Prophet с указанием праздников
        model = Prophet(holidays=holidays)

        # Обучаем модель на наших данных
        model.fit(df)

        # Создаем DataFrame для будущих дат
        future = model.make_future_dataframe(periods=3, freq='M')

        # Прогнозируем будущие продажи
        forecast = model.predict(future)

        # Выводим прогноз
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(3))

        # Визуализация прогноза
        fig = model.plot(forecast)
        plt.show()

        # Визуализация компонентов прогноза
        fig2 = model.plot_components(forecast)
        plt.show()
    except PermissionError:
        print(f"Ошибка прав доступа к файлу: {file_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
